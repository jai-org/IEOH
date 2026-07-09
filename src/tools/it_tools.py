from langchain.tools import tool
from typing import Dict, Any
import json
from src.core.utils import generate_ticket_id, get_timestamp, load_json_data, save_json_data

@tool
def create_it_ticket(employee_id: str, category: str, description: str, priority: str = "medium") -> Dict[str, Any]:
    """
    Create a new IT support ticket for an employee.
    
    Args:
        employee_id: Employee ID (e.g., EMP001)
        category: Ticket category (password_reset, software_install, hardware_issue, access_request)
        description: Detailed description of the issue
        priority: Priority level (low, medium, high)
    
    Returns:
        dict: Ticket creation result with ticket ID
    """
    ticket_id = generate_ticket_id()
    
    tickets = load_json_data("data/tickets.json") or []
    
    new_ticket = {
        "ticket_id": ticket_id,
        "employee_id": employee_id,
        "category": category,
        "priority": priority,
        "status": "open",
        "description": description,
        "created_at": get_timestamp(),
        "assigned_to": "IT Support"
    }
    
    tickets.append(new_ticket)
    save_json_data("data/tickets.json", tickets)
    
    return {
        "status": "success",
        "ticket_id": ticket_id,
        "message": f"IT ticket {ticket_id} created successfully",
        "ticket": new_ticket
    }

@tool
def reset_password(employee_id: str, email: str) -> Dict[str, Any]:
    """
    Reset password for an employee and send reset link to their email.
    
    Args:
        employee_id: Employee ID
        email: Employee email address
    
    Returns:
        dict: Password reset result
    """
    employees = load_json_data("data/employees.json") or []
    
    employee = next((emp for emp in employees if emp["employee_id"] == employee_id), None)
    
    if not employee:
        return {
            "status": "error",
            "message": f"Employee {employee_id} not found"
        }
    
    if employee["email"] != email:
        return {
            "status": "error",
            "message": "Email does not match employee record"
        }
    
    reset_link = f"https://company.com/reset-password?token={employee_id}_{get_timestamp()}"
    
    return {
        "status": "success",
        "message": f"Password reset link sent to {email}",
        "reset_link": reset_link,
        "employee_id": employee_id
    }

@tool
def check_ticket_status(ticket_id: str) -> Dict[str, Any]:
    """
    Check the status of an existing IT ticket.
    
    Args:
        ticket_id: Ticket ID to check
    
    Returns:
        dict: Ticket status and details
    """
    tickets = load_json_data("data/tickets.json") or []
    
    ticket = next((t for t in tickets if t["ticket_id"] == ticket_id), None)
    
    if not ticket:
        return {
            "status": "error",
            "message": f"Ticket {ticket_id} not found"
        }
    
    return {
        "status": "success",
        "ticket": ticket
    }

@tool
def grant_system_access(employee_id: str, system_name: str, access_level: str) -> Dict[str, Any]:
    """
    Grant system access to an employee.
    
    Args:
        employee_id: Employee ID
        system_name: Name of the system (e.g., CRM, ERP, Database)
        access_level: Access level (read, write, admin)
    
    Returns:
        dict: Access grant result
    """
    employees = load_json_data("data/employees.json") or []
    
    employee = next((emp for emp in employees if emp["employee_id"] == employee_id), None)
    
    if not employee:
        return {
            "status": "error",
            "message": f"Employee {employee_id} not found"
        }
    
    return {
        "status": "success",
        "message": f"Access granted to {employee['name']} for {system_name} with {access_level} permissions",
        "employee_id": employee_id,
        "system": system_name,
        "access_level": access_level,
        "granted_at": get_timestamp()
    }

@tool
def search_knowledge_base(query: str) -> Dict[str, Any]:
    """
    Search the IT knowledge base for solutions to common problems.
    
    Args:
        query: Search query
    
    Returns:
        dict: Search results with relevant articles
    """
    kb_articles = {
        "password": {
            "title": "How to Reset Your Password",
            "solution": "Use the self-service portal or contact IT support. Password must be 12+ characters with uppercase, lowercase, numbers, and symbols.",
            "category": "Authentication"
        },
        "vpn": {
            "title": "VPN Connection Issues",
            "solution": "1. Check internet connection 2. Verify VPN credentials 3. Restart VPN client 4. Contact IT if issue persists",
            "category": "Network"
        },
        "email": {
            "title": "Email Access Problems",
            "solution": "Clear browser cache, check email settings, verify password, or reset password if needed.",
            "category": "Email"
        },
        "software": {
            "title": "Software Installation",
            "solution": "Submit a ticket with software name and business justification. IT will review and install if approved.",
            "category": "Software"
        }
    }
    
    query_lower = query.lower()
    results = []
    
    for key, article in kb_articles.items():
        if key in query_lower or query_lower in article["title"].lower():
            results.append(article)
    
    if not results:
        results.append({
            "title": "No exact match found",
            "solution": "Please create a support ticket for personalized assistance",
            "category": "General"
        })
    
    return {
        "status": "success",
        "query": query,
        "results": results
    }
