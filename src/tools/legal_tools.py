from langchain.tools import tool
from typing import Dict, Any
from src.core.utils import get_timestamp, load_json_data, save_json_data


@tool
def create_contract(contract_name: str, counterparty: str, contract_type: str, owner_id: str) -> Dict[str, Any]:
    """Create a contract record."""
    if not all([contract_name.strip(), counterparty.strip(), contract_type.strip(), owner_id.strip()]):
        return {"status": "error", "message": "contract_name, counterparty, contract_type, and owner_id are required"}

    contracts = load_json_data("data/contracts.json") or []
    contract_id = f"CTR{len(contracts) + 1:03d}"
    contract = {
        "contract_id": contract_id,
        "contract_name": contract_name.strip(),
        "counterparty": counterparty.strip(),
        "contract_type": contract_type.strip(),
        "owner_id": owner_id.strip(),
        "status": "draft",
        "risk_level": "pending_review",
        "created_at": get_timestamp(),
    }
    contracts.append(contract)
    save_json_data("data/contracts.json", contracts)
    return {"status": "success", "message": f"Contract {contract_id} created", "contract": contract}


@tool
def review_contract_risk(contract_id: str, notes: str = "") -> Dict[str, Any]:
    """Return a lightweight risk assessment for a contract."""
    contracts = load_json_data("data/contracts.json") or []
    contract = next((c for c in contracts if c.get("contract_id") == contract_id), None)
    if not contract:
        return {"status": "error", "message": f"Contract {contract_id} not found"}

    ctype = contract.get("contract_type", "").lower()
    if any(k in ctype for k in ["msa", "data", "security"]):
        risk = "medium"
    elif any(k in ctype for k in ["nda", "standard"]):
        risk = "low"
    else:
        risk = "medium"

    contract["risk_level"] = risk
    contract["review_notes"] = notes
    contract["reviewed_at"] = get_timestamp()
    save_json_data("data/contracts.json", contracts)
    return {"status": "success", "contract_id": contract_id, "risk_level": risk, "notes": notes}


@tool
def check_compliance(topic: str) -> Dict[str, Any]:
    """Return basic compliance guidance."""
    guidance = {
        "privacy": "Ensure DPIA completion, lawful basis documented, and retention policy applied.",
        "security": "Verify encryption at rest/in transit, access controls, and audit logging.",
        "vendor": "Confirm DPA, security questionnaire, and SLA obligations are signed.",
        "employment": "Validate policy alignment, notice periods, and jurisdictional requirements.",
    }
    key = topic.lower().strip()
    result = guidance.get(key)
    if not result:
        return {"status": "success", "message": "No specific guidance found", "available_topics": list(guidance.keys())}
    return {"status": "success", "topic": key, "guidance": result}


@tool
def get_contract_status(contract_id: str) -> Dict[str, Any]:
    """Get contract lifecycle status."""
    contracts = load_json_data("data/contracts.json") or []
    contract = next((c for c in contracts if c.get("contract_id") == contract_id), None)
    if not contract:
        return {"status": "error", "message": f"Contract {contract_id} not found"}
    return {"status": "success", "contract": contract}


@tool
def update_contract_status(contract_id: str, status: str) -> Dict[str, Any]:
    """Update contract lifecycle status."""
    allowed = {"draft", "review", "approved", "signed", "expired"}
    normalized = status.lower().strip()
    if normalized not in allowed:
        return {"status": "error", "message": f"Invalid status. Allowed: {', '.join(sorted(allowed))}"}

    contracts = load_json_data("data/contracts.json") or []
    contract = next((c for c in contracts if c.get("contract_id") == contract_id), None)
    if not contract:
        return {"status": "error", "message": f"Contract {contract_id} not found"}

    contract["status"] = normalized
    contract["updated_at"] = get_timestamp()
    save_json_data("data/contracts.json", contracts)
    return {"status": "success", "message": f"Contract {contract_id} moved to {normalized}", "contract": contract}
