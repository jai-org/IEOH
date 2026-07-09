from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from sqlalchemy import DateTime, Float, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

from src.config import settings


class Base(DeclarativeBase):
    pass


class WorkflowRun(Base):
    __tablename__ = "workflow_runs"

    run_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    session_id: Mapped[str] = mapped_column(String(128), index=True)
    workflow_type: Mapped[str] = mapped_column(String(64))
    request_text: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class WorkflowMetric(Base):
    __tablename__ = "workflow_metrics"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(String(64), index=True)
    total_tasks: Mapped[int] = mapped_column(Integer, default=0)
    completed_tasks: Mapped[int] = mapped_column(Integer, default=0)
    pending_approvals: Mapped[int] = mapped_column(Integer, default=0)
    automation_rate_percent: Mapped[float] = mapped_column(Float, default=0.0)
    estimated_manual_minutes_saved: Mapped[int] = mapped_column(Integer, default=0)
    recorded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)


class WorkflowAuditEvent(Base):
    __tablename__ = "workflow_audit_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    run_id: Mapped[str] = mapped_column(String(64), index=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, index=True)
    event: Mapped[str] = mapped_column(String(128))
    detail: Mapped[str] = mapped_column(Text)


class WorkflowApproval(Base):
    __tablename__ = "workflow_approvals"

    approval_id: Mapped[str] = mapped_column(String(64), primary_key=True)
    run_id: Mapped[str] = mapped_column(String(64), index=True)
    department: Mapped[str] = mapped_column(String(64))
    action: Mapped[str] = mapped_column(Text)
    reason: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(32), default="pending", index=True)
    decided_by: Mapped[str | None] = mapped_column(String(64), nullable=True)
    decided_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    metadata_json: Mapped[str] = mapped_column(Text, default="{}")


def _db_path() -> Path:
    path = Path(settings.DATABASE_PATH)
    if not path.is_absolute():
        path = Path.cwd() / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


_ENGINE = create_engine(f"sqlite:///{_db_path()}", future=True)
_Session = sessionmaker(bind=_ENGINE, future=True)
Base.metadata.create_all(_ENGINE)


def persist_workflow_execution(
    *,
    run_id: str,
    session_id: str,
    request_text: str,
    workflow_type: str,
    status: str,
    execution_dashboard: Dict[str, Any],
) -> None:
    with _Session() as session:
        run = session.get(WorkflowRun, run_id)
        if not run:
            run = WorkflowRun(
                run_id=run_id,
                session_id=session_id,
                workflow_type=workflow_type,
                request_text=request_text,
                status=status,
            )
            session.add(run)
        else:
            run.status = status
        if status in {"completed", "error"}:
            run.completed_at = datetime.utcnow()

        metrics = execution_dashboard.get("metrics", {})
        session.add(
            WorkflowMetric(
                run_id=run_id,
                total_tasks=int(metrics.get("total_tasks", 0)),
                completed_tasks=int(metrics.get("completed_tasks", 0)),
                pending_approvals=int(metrics.get("pending_approvals", 0)),
                automation_rate_percent=float(metrics.get("automation_rate_percent", 0.0)),
                estimated_manual_minutes_saved=int(metrics.get("estimated_manual_minutes_saved", 0)),
            )
        )

        for event in execution_dashboard.get("audit_trail", []):
            event_ts = event.get("timestamp")
            try:
                parsed_ts = datetime.fromisoformat(event_ts) if event_ts else datetime.utcnow()
            except ValueError:
                parsed_ts = datetime.utcnow()

            session.add(
                WorkflowAuditEvent(
                    run_id=run_id,
                    timestamp=parsed_ts,
                    event=str(event.get("event", "UnknownEvent")),
                    detail=str(event.get("detail", "")),
                )
            )

        for approval in execution_dashboard.get("approvals_pending", []):
            approval_id = str(approval.get("approval_id", ""))
            if not approval_id:
                continue
            existing = session.get(WorkflowApproval, approval_id)
            payload = json.dumps(approval, default=str)
            if existing:
                existing.run_id = run_id
                existing.department = str(approval.get("department", ""))
                existing.action = str(approval.get("action", ""))
                existing.reason = str(approval.get("reason", ""))
                existing.status = str(approval.get("status", "pending"))
                existing.metadata_json = payload
            else:
                session.add(
                    WorkflowApproval(
                        approval_id=approval_id,
                        run_id=run_id,
                        department=str(approval.get("department", "")),
                        action=str(approval.get("action", "")),
                        reason=str(approval.get("reason", "")),
                        status=str(approval.get("status", "pending")),
                        metadata_json=payload,
                    )
                )

        session.commit()


def get_pending_approvals(limit: int = 50) -> List[Dict[str, Any]]:
    with _Session() as session:
        rows = (
            session.execute(
                select(WorkflowApproval)
                .where(WorkflowApproval.status == "pending")
                .order_by(WorkflowApproval.approval_id.desc())
                .limit(limit)
            )
            .scalars()
            .all()
        )
        return [
            {
                "approval_id": r.approval_id,
                "run_id": r.run_id,
                "department": r.department,
                "action": r.action,
                "reason": r.reason,
                "status": r.status,
            }
            for r in rows
        ]


def decide_approval(approval_id: str, decision: str, decided_by: str) -> bool:
    normalized = decision.lower().strip()
    if normalized not in {"approved", "rejected"}:
        return False

    with _Session() as session:
        approval = session.get(WorkflowApproval, approval_id)
        if not approval:
            return False
        approval.status = normalized
        approval.decided_by = decided_by.strip() or "approver"
        approval.decided_at = datetime.utcnow()
        session.commit()
        return True


def get_recent_workflow_runs(limit: int = 30) -> List[Dict[str, Any]]:
    with _Session() as session:
        runs = (
            session.execute(select(WorkflowRun).order_by(WorkflowRun.created_at.desc()).limit(limit))
            .scalars()
            .all()
        )

        output: List[Dict[str, Any]] = []
        for run in runs:
            latest_metric = (
                session.execute(
                    select(WorkflowMetric)
                    .where(WorkflowMetric.run_id == run.run_id)
                    .order_by(WorkflowMetric.recorded_at.desc())
                    .limit(1)
                )
                .scalars()
                .first()
            )
            output.append(
                {
                    "run_id": run.run_id,
                    "session_id": run.session_id,
                    "workflow_type": run.workflow_type,
                    "status": run.status,
                    "created_at": run.created_at.isoformat(),
                    "completed_at": run.completed_at.isoformat() if run.completed_at else None,
                    "automation_rate_percent": latest_metric.automation_rate_percent if latest_metric else 0.0,
                    "estimated_manual_minutes_saved": latest_metric.estimated_manual_minutes_saved if latest_metric else 0,
                }
            )
        return output
