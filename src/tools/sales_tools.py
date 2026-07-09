from langchain.tools import tool
from typing import Dict, Any
from src.core.utils import get_timestamp, load_json_data, save_json_data


@tool
def create_lead(customer_name: str, company: str, email: str, source: str) -> Dict[str, Any]:
    """Create a new sales lead."""
    if not customer_name.strip() or not company.strip() or not email.strip():
        return {"status": "error", "message": "customer_name, company, and email are required"}

    leads = load_json_data("data/leads.json") or []
    lead_id = f"LEAD{len(leads) + 1:03d}"
    new_lead = {
        "lead_id": lead_id,
        "customer_name": customer_name.strip(),
        "company": company.strip(),
        "email": email.strip(),
        "source": source.strip() if source else "unknown",
        "status": "new",
        "created_at": get_timestamp(),
    }
    leads.append(new_lead)
    save_json_data("data/leads.json", leads)

    return {"status": "success", "message": f"Lead {lead_id} created", "lead": new_lead}


@tool
def update_opportunity_stage(lead_id: str, stage: str, notes: str = "") -> Dict[str, Any]:
    """Update a lead/opportunity stage."""
    stages = {"new", "qualified", "proposal", "negotiation", "won", "lost"}
    stage_normalized = stage.lower().strip()
    if stage_normalized not in stages:
        return {"status": "error", "message": f"Invalid stage. Allowed: {', '.join(sorted(stages))}"}

    leads = load_json_data("data/leads.json") or []
    lead = next((l for l in leads if l.get("lead_id") == lead_id), None)
    if not lead:
        return {"status": "error", "message": f"Lead {lead_id} not found"}

    lead["status"] = stage_normalized
    lead["updated_at"] = get_timestamp()
    if notes:
        lead["notes"] = notes
    save_json_data("data/leads.json", leads)

    return {"status": "success", "message": f"Lead {lead_id} moved to {stage_normalized}", "lead": lead}


@tool
def get_lead_details(lead_id: str) -> Dict[str, Any]:
    """Get details of a lead."""
    leads = load_json_data("data/leads.json") or []
    lead = next((l for l in leads if l.get("lead_id") == lead_id), None)
    if not lead:
        return {"status": "error", "message": f"Lead {lead_id} not found"}
    return {"status": "success", "lead": lead}


@tool
def list_pipeline() -> Dict[str, Any]:
    """Return pipeline summary by stage."""
    leads = load_json_data("data/leads.json") or []
    summary: Dict[str, int] = {}
    for lead in leads:
        stage = lead.get("status", "unknown")
        summary[stage] = summary.get(stage, 0) + 1
    return {"status": "success", "total_leads": len(leads), "pipeline": summary}


@tool
def search_customer(customer_query: str) -> Dict[str, Any]:
    """Search leads by customer/company/email."""
    query = customer_query.lower().strip()
    if not query:
        return {"status": "error", "message": "customer_query is required"}

    leads = load_json_data("data/leads.json") or []
    matches = [
        lead
        for lead in leads
        if query in lead.get("customer_name", "").lower()
        or query in lead.get("company", "").lower()
        or query in lead.get("email", "").lower()
    ]
    return {"status": "success", "count": len(matches), "results": matches}
