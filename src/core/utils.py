import json
import re
import uuid
from datetime import datetime
from typing import Dict, Any, List

def generate_session_id() -> str:
    return str(uuid.uuid4())

def generate_ticket_id() -> str:
    return f"TKT{uuid.uuid4().hex[:8].upper()}"

def generate_expense_id() -> str:
    return f"EXP{uuid.uuid4().hex[:8].upper()}"

def generate_po_id() -> str:
    return f"PO{uuid.uuid4().hex[:8].upper()}"

def get_timestamp() -> str:
    return datetime.now().isoformat()

def format_response(
    status: str,
    message: str,
    data: Any = None,
    agent: str = None
) -> Dict[str, Any]:
    response = {
        "status": status,
        "message": message,
        "timestamp": get_timestamp()
    }
    if data:
        response["data"] = data
    if agent:
        response["agent"] = agent
    return response

def parse_user_intent(user_request: str) -> Dict[str, Any]:
    user_request_lower = user_request.lower()
    tokens = set(re.findall(r"\b[a-z0-9_]+\b", user_request_lower))
    
    intent_keywords = {
        "it": ["password", "reset", "access", "login", "ticket", "system", "computer", "laptop", "software"],
        "hr": ["leave", "vacation", "pto", "onboard", "employee", "policy", "benefits", "payroll"],
        "finance": ["expense", "budget", "invoice", "payment", "reimbursement", "cost", "financial"],
        "procurement": ["purchase", "order", "vendor", "supplier", "buy", "procurement", "contract"],
        "sales": ["lead", "opportunity", "customer", "crm", "deal", "sales", "prospect"],
        "marketing": ["campaign", "content", "marketing", "social", "email campaign", "advertisement"],
        "legal": ["contract", "legal", "compliance", "review", "agreement", "terms"]
    }
    
    dept_scores = {}
    for dept, keywords in intent_keywords.items():
        score = 0
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Higher confidence for exact phrase hit.
            if keyword_lower in user_request_lower:
                score += 2
            # Token hit helps avoid over-counting broad substring matches.
            keyword_tokens = keyword_lower.split()
            if len(keyword_tokens) == 1 and keyword_tokens[0] in tokens:
                score += 1
        if score > 0:
            dept_scores[dept] = score

    priority_order = list(intent_keywords.keys())
    detected_departments = sorted(
        dept_scores.keys(),
        key=lambda d: (-dept_scores[d], priority_order.index(d))
    )
    
    return {
        "departments": detected_departments,
        "primary_department": detected_departments[0] if detected_departments else "general",
        "is_multi_department": len(detected_departments) > 1
    }


def parse_friendly_date(date_text: str) -> str:
    """Parse human-readable dates and return ISO YYYY-MM-DD; fallback to raw text."""
    if not date_text:
        return ""

    raw = date_text.strip().replace(",", "")
    date_formats = [
        "%Y-%m-%d",
        "%d-%m-%Y",
        "%B %d %Y",
        "%b %d %Y",
        "%B %d",
        "%b %d",
    ]

    for fmt in date_formats:
        try:
            parsed = datetime.strptime(raw, fmt)
            if "%Y" not in fmt:
                parsed = parsed.replace(year=datetime.now().year)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue

    return raw


def parse_enterprise_onboarding_request(user_request: str) -> Dict[str, Any]:
    """Extract onboarding entities from natural language."""
    text = user_request.strip()
    lower = text.lower()

    name = ""
    role = ""
    location = ""
    start_date = ""
    manager = ""
    systems: List[str] = []
    laptop_preference = ""

    name_match = re.search(r"onboard\s+([a-zA-Z][a-zA-Z\s]+?)\s+as\b", text, re.IGNORECASE)
    if name_match:
        name = name_match.group(1).strip().rstrip(".")

    role_match = re.search(r"\bas\s+(?:an?\s+)?([a-zA-Z][a-zA-Z\s]+?)\s+in\b", text, re.IGNORECASE)
    if role_match:
        role = role_match.group(1).strip().rstrip(".")

    location_match = re.search(r"\bin\s+([a-zA-Z][a-zA-Z\s]+?)\s+starting\b", text, re.IGNORECASE)
    if location_match:
        location = location_match.group(1).strip().rstrip(".")

    start_match = re.search(r"\bstarting\s+([a-zA-Z0-9,\-\s]+?)(?:\.|$)", text, re.IGNORECASE)
    if start_match:
        start_date = parse_friendly_date(start_match.group(1).strip())

    systems_match = re.search(r"\bneeds\s+(.+?)(?:\.|laptop preference:|manager:|$)", lower, re.IGNORECASE | re.DOTALL)
    if systems_match:
        systems_raw = systems_match.group(1).replace(" and ", ",")
        systems = [s.strip(" .").title() for s in systems_raw.split(",") if s.strip(" .")]

    laptop_match = re.search(r"laptop preference:\s*([a-zA-Z0-9\s\-]+?)(?:\.|$)", text, re.IGNORECASE)
    if laptop_match:
        laptop_preference = laptop_match.group(1).strip().rstrip(".")

    manager_match = re.search(r"manager:\s*([a-zA-Z][a-zA-Z\s]+?)(?:\.|$)", text, re.IGNORECASE)
    if manager_match:
        manager = manager_match.group(1).strip().rstrip(".")

    return {
        "employee_name": name or "New Employee",
        "role": role or "Analyst",
        "location": location or "Unknown",
        "start_date": start_date or datetime.now().strftime("%Y-%m-%d"),
        "systems": systems,
        "laptop_preference": laptop_preference or "Standard Laptop",
        "manager_name": manager or "Hiring Manager",
    }

def load_json_data(filepath: str) -> Any:
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None

def save_json_data(filepath: str, data: Any) -> bool:
    try:
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False
