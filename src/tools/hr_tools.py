from langchain.tools import tool
from typing import Dict, Any
from datetime import datetime
from src.core.utils import get_timestamp, load_json_data, save_json_data

@tool
def request_leave(employee_id: str, start_date: str, end_date: str, leave_type: str, reason: str = "") -> Dict[str, Any]:
    """
    Submit a leave request for an employee.
    
    Args:
        employee_id: Employee ID
        start_date: Leave start date (YYYY-MM-DD)
        end_date: Leave end date (YYYY-MM-DD)
        leave_type: Type of leave (vacation, sick, personal, unpaid)
        reason: Optional reason for leave
    
    Returns:
        dict: Leave request result
    """
    employees = load_json_data("data/employees.json") or []
    
    employee = next((emp for emp in employees if emp["employee_id"] == employee_id), None)
    
    if not employee:
        return {
            "status": "error",
            "message": f"Employee {employee_id} not found"
        }
    
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        days_requested = (end - start).days + 1
    except ValueError:
        return {
            "status": "error",
            "message": "Invalid date format. Use YYYY-MM-DD"
        }
    
    if end < start:
        return {
            "status": "error",
            "message": "End date cannot be before start date"
        }

    if days_requested <= 0:
        return {
            "status": "error",
            "message": "Leave duration must be at least 1 day"
        }

    allowed_leave_types = {"vacation", "sick", "personal", "unpaid"}
    leave_type_normalized = leave_type.lower().strip()
    if leave_type_normalized not in allowed_leave_types:
        return {
            "status": "error",
            "message": f"Invalid leave type: {leave_type}. Allowed: {', '.join(sorted(allowed_leave_types))}"
        }

    leave_balance = employee.get("leave_balance", 0)
    
    if days_requested > leave_balance and leave_type_normalized == "vacation":
        return {
            "status": "error",
            "message": f"Insufficient leave balance. Requested: {days_requested} days, Available: {leave_balance} days"
        }
    
    leave_request_id = f"LR{employee_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    return {
        "status": "success",
        "message": f"Leave request submitted successfully for {days_requested} days",
        "leave_request_id": leave_request_id,
        "employee_id": employee_id,
        "employee_name": employee["name"],
        "start_date": start_date,
        "end_date": end_date,
        "days": days_requested,
        "leave_type": leave_type_normalized,
        "remaining_balance": leave_balance - days_requested if leave_type_normalized == "vacation" else leave_balance,
        "status_request": "pending_approval",
        "submitted_at": get_timestamp()
    }

@tool
def get_employee_info(employee_id: str) -> Dict[str, Any]:
    """
    Retrieve employee information from the database.
    
    Args:
        employee_id: Employee ID
    
    Returns:
        dict: Employee details
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
        "employee": employee
    }

@tool
def search_hr_policy(policy_topic: str) -> Dict[str, Any]:
    """
    Search HR policies and guidelines.
    
    Args:
        policy_topic: Topic to search (leave, benefits, code_of_conduct, remote_work, etc.)
    
    Returns:
        dict: Policy information
    """
    policies = {
        "leave": {
            "title": "Leave Policy",
            "summary": "Employees receive 20 days of paid vacation annually. Sick leave is 10 days per year. Leave requests must be submitted 2 weeks in advance for vacation.",
            "details": [
                "Vacation: 20 days/year",
                "Sick Leave: 10 days/year",
                "Personal Leave: 5 days/year",
                "Parental Leave: 12 weeks paid",
                "Advance notice: 2 weeks for vacation"
            ]
        },
        "benefits": {
            "title": "Employee Benefits",
            "summary": "Comprehensive benefits including health insurance, 401k matching, wellness programs, and professional development.",
            "details": [
                "Health Insurance: Medical, Dental, Vision",
                "401k: 5% company match",
                "Wellness: Gym membership reimbursement",
                "Learning: $2000/year for courses",
                "Life Insurance: 2x annual salary"
            ]
        },
        "remote_work": {
            "title": "Remote Work Policy",
            "summary": "Hybrid work model with 3 days in office, 2 days remote per week. Full remote available with manager approval.",
            "details": [
                "Hybrid: 3 office days, 2 remote days",
                "Full remote: Manager approval required",
                "Equipment: Company provides laptop and monitor",
                "Hours: Core hours 10am-3pm in your timezone",
                "Communication: Daily standup required"
            ]
        },
        "code_of_conduct": {
            "title": "Code of Conduct",
            "summary": "Professional behavior, respect, integrity, and ethical conduct expected from all employees.",
            "details": [
                "Respect and dignity for all",
                "Zero tolerance for harassment",
                "Confidentiality of company information",
                "Conflict of interest disclosure",
                "Report violations to HR"
            ]
        }
    }
    
    policy_topic_lower = policy_topic.lower()
    
    for key, policy in policies.items():
        if key in policy_topic_lower or policy_topic_lower in key:
            return {
                "status": "success",
                "policy": policy
            }
    
    return {
        "status": "success",
        "message": "No specific policy found. Please contact HR for more information.",
        "available_topics": list(policies.keys())
    }

@tool
def initiate_onboarding(employee_name: str, department: str, role: str, start_date: str, manager_id: str) -> Dict[str, Any]:
    """
    Initiate onboarding process for a new employee.
    
    Args:
        employee_name: Full name of new employee
        department: Department name
        role: Job role/title
        start_date: Start date (YYYY-MM-DD)
        manager_id: Manager's employee ID
    
    Returns:
        dict: Onboarding initiation result
    """
    employees = load_json_data("data/employees.json") or []
    
    new_employee_id = f"EMP{str(len(employees) + 1).zfill(3)}"
    email = f"{employee_name.lower().replace(' ', '.')}@company.com"
    
    new_employee = {
        "employee_id": new_employee_id,
        "name": employee_name,
        "email": email,
        "department": department,
        "role": role,
        "manager_id": manager_id,
        "start_date": start_date,
        "status": "onboarding",
        "leave_balance": 20
    }
    
    employees.append(new_employee)
    save_json_data("data/employees.json", employees)
    
    onboarding_tasks = [
        "Create employee profile - Completed",
        "Generate email address - Completed",
        "IT setup (laptop, accounts) - Pending",
        "Payroll setup - Pending",
        "Benefits enrollment - Pending",
        "Orientation scheduling - Pending"
    ]
    
    return {
        "status": "success",
        "message": f"Onboarding initiated for {employee_name}",
        "employee_id": new_employee_id,
        "email": email,
        "onboarding_tasks": onboarding_tasks,
        "next_steps": [
            "IT Agent will setup accounts and equipment",
            "Finance Agent will setup payroll",
            "HR will schedule orientation"
        ]
    }

@tool
def check_leave_balance(employee_id: str) -> Dict[str, Any]:
    """
    Check leave balance for an employee.
    
    Args:
        employee_id: Employee ID
    
    Returns:
        dict: Leave balance information
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
        "employee_id": employee_id,
        "employee_name": employee["name"],
        "leave_balance": employee.get("leave_balance", 0),
        "message": f"{employee['name']} has {employee.get('leave_balance', 0)} days of leave remaining"
    }
