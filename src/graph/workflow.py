from datetime import datetime
import uuid
from typing import Dict, Any, Literal, List

from langgraph.graph import StateGraph, END

from src.core import AgentState, parse_user_intent
from src.core.utils import parse_enterprise_onboarding_request, load_json_data
from src.core.enterprise_store import persist_workflow_execution
from src.agents import (
    OrchestratorAgent,
    ITSupportAgent,
    HROperationsAgent,
    FinanceAgent,
    ProcurementAgent,
    SalesAgent,
    MarketingAgent,
    LegalAgent,
)
from src.tools import (
    initiate_onboarding,
    search_hr_policy,
    create_it_ticket,
    grant_system_access,
    analyze_budget,
    search_vendors,
    create_purchase_order,
    check_compliance,
)

orchestrator = OrchestratorAgent()
it_agent = ITSupportAgent()
hr_agent = HROperationsAgent()
finance_agent = FinanceAgent()
procurement_agent = ProcurementAgent()
sales_agent = SalesAgent()
marketing_agent = MarketingAgent()
legal_agent = LegalAgent()


def _is_enterprise_onboarding_request(user_request: str) -> bool:
    text = user_request.lower()
    # Hard fallback: any onboarding-style request should use structured enterprise flow.
    if "onboard" in text:
        return True
    return "onboarding" in text and ("employee" in text or "manager" in text)


def _resolve_manager_id(manager_name: str) -> str:
    employees = load_json_data("data/employees.json") or []
    manager = next((e for e in employees if e.get("name", "").lower() == manager_name.lower()), None)
    if manager:
        return manager.get("employee_id", "EMP050")
    normalized = manager_name.strip().upper().replace(" ", "_")
    return f"MGR_{normalized}"[:16]


def _guess_department(role: str) -> str:
    role_lower = role.lower()
    if any(k in role_lower for k in ["analyst", "data", "engineer", "developer"]):
        return "Engineering"
    if "marketing" in role_lower:
        return "Marketing"
    if "sales" in role_lower:
        return "Sales"
    if "finance" in role_lower:
        return "Finance"
    return "HR"


def _add_audit(execution: Dict[str, Any], event: str, detail: str) -> None:
    execution["audit_trail"].append(
        {
            "timestamp": datetime.now().isoformat(),
            "event": event,
            "detail": detail,
        }
    )


def _add_task(
    execution: Dict[str, Any],
    department: str,
    agent: str,
    task: str,
    status: str,
    detail: str,
    task_id: str = "",
) -> None:
    execution["tasks"].append(
        {
            "task_id": task_id or f"T{len(execution['tasks']) + 1:03d}",
            "department": department,
            "agent": agent,
            "task": task,
            "status": status,
            "detail": detail,
            "timestamp": datetime.now().isoformat(),
        }
    )


def orchestrator_node(state: AgentState) -> AgentState:
    """Orchestrator analyzes request and routes to appropriate agent."""
    user_request = state["user_request"]

    state["metadata"] = state.get("metadata", {})
    state["metadata"]["pending_departments"] = []
    state["current_agent"] = "orchestrator"

    if _is_enterprise_onboarding_request(user_request):
        parsed = parse_enterprise_onboarding_request(user_request)
        state["metadata"]["enterprise_onboarding"] = parsed
        state["target_agent"] = "enterprise_onboarding"
        state["workflow_type"] = "enterprise_onboarding"
        state["agent_responses"] = state.get("agent_responses", [])
        state["agent_responses"].append(
            {
                "agent": "Orchestrator",
                "message": "I detected a full onboarding workflow. I am creating tasks across HR, IT, Finance, Procurement, and Legal with approval gates.",
                "target": "enterprise_onboarding",
            }
        )
        return state

    intent = parse_user_intent(user_request)
    target_agent = intent["primary_department"]

    state["target_agent"] = target_agent
    state["workflow_type"] = "single" if not intent["is_multi_department"] else "multi"

    if intent["is_multi_department"]:
        departments: List[str] = intent.get("departments", [])
        if departments:
            state["target_agent"] = departments[0]
            state["metadata"]["pending_departments"] = departments[1:]

    orchestrator_response = {
        "agent": "Orchestrator",
        "message": f"I'll route your request to the {state['target_agent'].upper()} department.",
        "target": state["target_agent"],
    }

    if target_agent == "general":
        orchestrator_response["message"] = (
            "I can help with IT, HR, Finance, Procurement, Sales, Marketing, and Legal requests. "
            "Please share details like employee ID, ticket/expense ID, campaign/lead ID, or contract/vendor details."
        )
        state["final_response"] = orchestrator_response["message"]
        state["status"] = "completed"

    state["agent_responses"] = state.get("agent_responses", [])
    state["agent_responses"].append(orchestrator_response)
    return state


def _advance_multi_workflow(state: AgentState) -> None:
    pending = state.get("metadata", {}).get("pending_departments", [])
    if pending:
        next_target = pending.pop(0)
        state["metadata"]["pending_departments"] = pending
        state["target_agent"] = next_target
        state["status"] = "in_progress"
    else:
        state["target_agent"] = "end"
        state["status"] = "completed"


def enterprise_onboarding_node(state: AgentState) -> AgentState:
    """Execute a structured cross-department onboarding workflow."""
    state["current_agent"] = "enterprise_orchestrator"
    details = state.get("metadata", {}).get("enterprise_onboarding", {})

    run_id = f"RUN-{uuid.uuid4().hex[:10].upper()}"
    execution: Dict[str, Any] = {
        "run_id": run_id,
        "request_type": "enterprise_onboarding",
        "parsed_request": details,
        "tasks": [],
        "approvals_pending": [],
        "documents": [],
        "emails": [],
        "audit_trail": [],
        "metrics": {},
    }

    state["agent_responses"] = state.get("agent_responses", [])
    _add_audit(execution, "WorkflowStarted", "Enterprise onboarding workflow started.")

    employee_name = details.get("employee_name", "New Employee")
    role = details.get("role", "Analyst")
    start_date = details.get("start_date", datetime.now().strftime("%Y-%m-%d"))
    location = details.get("location", "Unknown")
    systems = details.get("systems", [])
    laptop_preference = details.get("laptop_preference", "Standard Laptop")
    manager_name = details.get("manager_name", "Hiring Manager")
    manager_id = _resolve_manager_id(manager_name)
    department = _guess_department(role)

    # HR onboarding
    hr_result = initiate_onboarding.invoke(
        {
            "employee_name": employee_name,
            "department": department,
            "role": role,
            "start_date": start_date,
            "manager_id": manager_id,
        }
    )
    employee_id = hr_result.get("employee_id", state.get("user_id", "EMP001"))
    employee_email = hr_result.get("email", f"{employee_name.lower().replace(' ', '.')}@company.com")
    _add_task(execution, "HR", "HR Operations Agent", "Initiate onboarding profile", hr_result.get("status", "error"), hr_result.get("message", "HR onboarding attempted"))
    _add_audit(execution, "HR.Onboarding", hr_result.get("message", "Onboarding profile attempted."))

    # Policy and compliance checks
    hr_policy = search_hr_policy.invoke({"policy_topic": "code_of_conduct"})
    _add_task(execution, "HR", "HR Operations Agent", "Check HR policies", hr_policy.get("status", "error"), "Validated onboarding-related HR policies.")

    compliance = check_compliance.invoke({"topic": "employment"})
    _add_task(execution, "Legal", "Legal Agent", "Check employment compliance", compliance.get("status", "error"), compliance.get("guidance", compliance.get("message", "Compliance check attempted")))

    budget = analyze_budget.invoke({"department": department if department in {"Engineering", "Marketing", "Sales", "Finance", "HR"} else "Engineering", "period": "monthly"})
    _add_task(execution, "Finance", "Finance Agent", "Check onboarding budget", budget.get("status", "error"), budget.get("analysis", {}).get("recommendation", budget.get("message", "Budget check attempted")))

    # IT setup and access
    risky_systems = {"jenkins", "github"}
    for system in systems:
        ticket = create_it_ticket.invoke(
            {
                "employee_id": employee_id,
                "category": "access_request",
                "description": f"Provision {system} access for {employee_name} ({role}) in {location}.",
                "priority": "high" if system.lower() in risky_systems else "medium",
            }
        )
        _add_task(execution, "IT", "IT Support Agent", f"Create access ticket for {system}", ticket.get("status", "error"), ticket.get("message", "Ticket creation attempted"))

        if system.lower() in risky_systems:
            approval_id = f"APR-{len(execution['approvals_pending']) + 1:03d}"
            approval_item = {
                "approval_id": approval_id,
                "department": "IT",
                "action": f"Grant {system} access",
                "reason": f"{system} is marked as sensitive and requires human approval.",
                "status": "pending",
            }
            execution["approvals_pending"].append(approval_item)
            _add_task(execution, "IT", "IT Support Agent", f"Grant {system} access", "pending_approval", f"Paused for human approval ({approval_id}).")
        else:
            access = grant_system_access.invoke({"employee_id": employee_id, "system_name": system, "access_level": "standard"})
            _add_task(execution, "IT", "IT Support Agent", f"Grant {system} access", access.get("status", "error"), access.get("message", "Access provisioning attempted"))

    # Procurement for laptop
    vendor_search = search_vendors.invoke({"category": "IT Equipment", "min_rating": 4.0})
    vendors = vendor_search.get("vendors", [])
    selected_vendor = next((v for v in vendors if "dell" in v.get("name", "").lower()), None)
    if not selected_vendor and vendors:
        selected_vendor = vendors[0]

    laptop_cost = 1450.0 if "macbook air" in laptop_preference.lower() else 1200.0
    if selected_vendor:
        po = create_purchase_order.invoke(
            {
                "vendor_id": selected_vendor["vendor_id"],
                "items": laptop_preference,
                "quantity": 1,
                "estimated_cost": laptop_cost,
                "requester_id": employee_id,
            }
        )
        _add_task(execution, "Procurement", "Procurement Agent", "Create laptop purchase order", po.get("status", "error"), po.get("message", "PO creation attempted"))

        if po.get("approval_required") or "macbook" in laptop_preference.lower():
            approval_id = f"APR-{len(execution['approvals_pending']) + 1:03d}"
            execution["approvals_pending"].append(
                {
                    "approval_id": approval_id,
                    "department": "Procurement",
                    "action": f"Approve laptop procurement ({laptop_preference})",
                    "reason": "Non-standard hardware or policy-triggered approval gate.",
                    "status": "pending",
                }
            )
            _add_task(execution, "Procurement", "Procurement Agent", "Approve laptop procurement", "pending_approval", f"Paused for human approval ({approval_id}).")

    # Documents and emails
    execution["documents"] = [
        {
            "title": "Onboarding Checklist",
            "type": "checklist",
            "content": (
                f"Employee: {employee_name}\nRole: {role}\nLocation: {location}\nStart Date: {start_date}\n"
                f"Manager: {manager_name}\nSystems: {', '.join(systems) if systems else 'None specified'}\n"
                f"Laptop: {laptop_preference}\n"
            ),
        },
        {
            "title": "Access Provisioning Sheet",
            "type": "document",
            "content": "\n".join([f"- {system}: Requested" for system in systems]) if systems else "- No systems requested",
        },
    ]
    execution["emails"] = [
        {
            "to": employee_email,
            "subject": f"Welcome to the team, {employee_name}",
            "body": f"Hi {employee_name}, your onboarding is in progress for {start_date}.",
        },
        {
            "to": f"{manager_name.lower().replace(' ', '.')}@company.com",
            "subject": f"Onboarding tracker for {employee_name}",
            "body": "Please review pending approvals and kickoff tasks in the dashboard.",
        },
        {
            "to": "it-support@company.com",
            "subject": f"Provisioning request for {employee_name}",
            "body": f"Please process requested systems: {', '.join(systems) if systems else 'No systems listed'}.",
        },
    ]

    _add_audit(execution, "ArtifactsGenerated", "Generated onboarding documents and email drafts.")

    total_tasks = len(execution["tasks"])
    completed_tasks = len([t for t in execution["tasks"] if t["status"] == "success"])
    pending_approvals = len(execution["approvals_pending"])
    automated_minutes_saved = completed_tasks * 15

    execution["metrics"] = {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_approvals": pending_approvals,
        "automation_rate_percent": round((completed_tasks / total_tasks * 100), 1) if total_tasks else 0,
        "estimated_manual_minutes_saved": automated_minutes_saved,
    }
    _add_audit(execution, "WorkflowMetrics", f"Completed {completed_tasks}/{total_tasks} tasks with {pending_approvals} approvals pending.")

    state["metadata"]["execution_dashboard"] = execution

    if pending_approvals > 0:
        state["status"] = "pending_approval"
        state["next_steps"] = [
            f"Review approval {a['approval_id']}: {a['action']}" for a in execution["approvals_pending"]
        ]
        state["final_response"] = (
            f"Onboarding plan created for {employee_name}. "
            f"{pending_approvals} risky actions are paused for human approval."
        )
    else:
        state["status"] = "completed"
        state["next_steps"] = ["Send welcome emails", "Track onboarding completion on Day 1"]
        state["final_response"] = f"Onboarding workflow for {employee_name} completed successfully."

    state["agent_responses"].extend(
        [
            {"agent": "HR Operations Agent", "message": f"Employee profile and onboarding initiated for {employee_name}."},
            {"agent": "IT Support Agent", "message": "Access tickets created and non-risky access provisioned automatically."},
            {"agent": "Finance Agent", "message": "Budget and cost checks completed for onboarding activities."},
            {"agent": "Procurement Agent", "message": f"Laptop procurement prepared for {laptop_preference}."},
            {"agent": "Legal Agent", "message": "Compliance checks completed and risky actions gated for approval."},
        ]
    )

    persist_workflow_execution(
        run_id=run_id,
        session_id=str(state.get("session_id", "")),
        request_text=str(state.get("user_request", "")),
        workflow_type="enterprise_onboarding",
        status=str(state.get("status", "completed")),
        execution_dashboard=execution,
    )

    state["target_agent"] = "end"
    return state


def _invoke_specialist_agent(state: AgentState, agent_name: str, executor) -> AgentState:
    state["current_agent"] = agent_name
    try:
        result = executor.invoke(state)
        state["agent_responses"] = state.get("agent_responses", [])
        state["agent_responses"].append(result)
        state["final_response"] = result.get("response", "")
        _advance_multi_workflow(state)
    except Exception as e:
        state["final_response"] = f"Error in {agent_name}: {str(e)}"
        state["status"] = "error"
    return state


def it_support_node(state: AgentState) -> AgentState:
    return _invoke_specialist_agent(state, "it_support", it_agent)


def hr_operations_node(state: AgentState) -> AgentState:
    return _invoke_specialist_agent(state, "hr_operations", hr_agent)


def finance_node(state: AgentState) -> AgentState:
    return _invoke_specialist_agent(state, "finance", finance_agent)


def procurement_node(state: AgentState) -> AgentState:
    return _invoke_specialist_agent(state, "procurement", procurement_agent)


def sales_node(state: AgentState) -> AgentState:
    return _invoke_specialist_agent(state, "sales", sales_agent)


def marketing_node(state: AgentState) -> AgentState:
    return _invoke_specialist_agent(state, "marketing", marketing_agent)


def legal_node(state: AgentState) -> AgentState:
    return _invoke_specialist_agent(state, "legal", legal_agent)


def route_to_agent(
    state: AgentState,
) -> Literal["enterprise_onboarding", "it_support", "hr_operations", "finance", "procurement", "sales", "marketing", "legal", "end"]:
    target = state.get("target_agent", "end")
    routing = {
        "enterprise_onboarding": "enterprise_onboarding",
        "it": "it_support",
        "hr": "hr_operations",
        "finance": "finance",
        "procurement": "procurement",
        "sales": "sales",
        "marketing": "marketing",
        "legal": "legal",
    }
    return routing.get(target, "end")


def route_after_agent(
    state: AgentState,
) -> Literal["enterprise_onboarding", "it_support", "hr_operations", "finance", "procurement", "sales", "marketing", "legal", "end"]:
    return route_to_agent(state)


def build_workflow() -> StateGraph:
    workflow = StateGraph(AgentState)
    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("enterprise_onboarding", enterprise_onboarding_node)
    workflow.add_node("it_support", it_support_node)
    workflow.add_node("hr_operations", hr_operations_node)
    workflow.add_node("finance", finance_node)
    workflow.add_node("procurement", procurement_node)
    workflow.add_node("sales", sales_node)
    workflow.add_node("marketing", marketing_node)
    workflow.add_node("legal", legal_node)

    workflow.set_entry_point("orchestrator")

    mapping = {
        "enterprise_onboarding": "enterprise_onboarding",
        "it_support": "it_support",
        "hr_operations": "hr_operations",
        "finance": "finance",
        "procurement": "procurement",
        "sales": "sales",
        "marketing": "marketing",
        "legal": "legal",
        "end": END,
    }

    workflow.add_conditional_edges("orchestrator", route_to_agent, mapping)
    workflow.add_edge("enterprise_onboarding", END)

    for node_name in [
        "it_support",
        "hr_operations",
        "finance",
        "procurement",
        "sales",
        "marketing",
        "legal",
    ]:
        workflow.add_conditional_edges(node_name, route_after_agent, mapping)

    return workflow.compile()


app = build_workflow()
