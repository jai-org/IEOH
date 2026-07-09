from langchain.tools import tool
from typing import Dict, Any
from src.core.utils import get_timestamp, load_json_data, save_json_data

@tool
def approve_expense(expense_id: str, approver_id: str, comments: str = "") -> Dict[str, Any]:
    """
    Approve an expense report.
    
    Args:
        expense_id: Expense ID to approve
        approver_id: ID of the person approving
        comments: Optional approval comments
    
    Returns:
        dict: Approval result
    """
    expenses = load_json_data("data/expenses.json") or []
    
    expense = next((exp for exp in expenses if exp["expense_id"] == expense_id), None)
    
    if not expense:
        return {
            "status": "error",
            "message": f"Expense {expense_id} not found"
        }
    
    if expense["status"] != "pending_approval":
        return {
            "status": "error",
            "message": f"Expense {expense_id} is not pending approval. Current status: {expense['status']}"
        }
    
    expense["status"] = "approved"
    expense["approved_by"] = approver_id
    expense["approved_at"] = get_timestamp()
    expense["approval_comments"] = comments
    
    save_json_data("data/expenses.json", expenses)
    
    return {
        "status": "success",
        "message": f"Expense {expense_id} approved successfully",
        "expense_id": expense_id,
        "amount": expense["amount"],
        "approved_by": approver_id,
        "approved_at": expense["approved_at"]
    }

@tool
def get_expense_details(expense_id: str) -> Dict[str, Any]:
    """
    Retrieve details of an expense report.
    
    Args:
        expense_id: Expense ID
    
    Returns:
        dict: Expense details
    """
    expenses = load_json_data("data/expenses.json") or []
    
    expense = next((exp for exp in expenses if exp["expense_id"] == expense_id), None)
    
    if not expense:
        return {
            "status": "error",
            "message": f"Expense {expense_id} not found"
        }
    
    return {
        "status": "success",
        "expense": expense
    }

@tool
def analyze_budget(department: str, period: str = "monthly") -> Dict[str, Any]:
    """
    Analyze budget for a department.
    
    Args:
        department: Department name
        period: Analysis period (monthly, quarterly, yearly)
    
    Returns:
        dict: Budget analysis
    """
    budget_data = {
        "Engineering": {
            "allocated": 500000,
            "spent": 425000,
            "remaining": 75000,
            "utilization": 85
        },
        "Marketing": {
            "allocated": 300000,
            "spent": 275000,
            "remaining": 25000,
            "utilization": 91.7
        },
        "Sales": {
            "allocated": 400000,
            "spent": 350000,
            "remaining": 50000,
            "utilization": 87.5
        },
        "Finance": {
            "allocated": 200000,
            "spent": 150000,
            "remaining": 50000,
            "utilization": 75
        },
        "HR": {
            "allocated": 250000,
            "spent": 200000,
            "remaining": 50000,
            "utilization": 80
        }
    }
    
    dept_budget = budget_data.get(department)
    
    if not dept_budget:
        return {
            "status": "error",
            "message": f"Budget data not found for department: {department}",
            "available_departments": list(budget_data.keys())
        }
    
    return {
        "status": "success",
        "department": department,
        "period": period,
        "budget": dept_budget,
        "analysis": {
            "status": "healthy" if dept_budget["utilization"] < 90 else "warning",
            "recommendation": "Budget utilization is within acceptable range" if dept_budget["utilization"] < 90 else "Consider budget adjustment or expense reduction"
        }
    }

@tool
def process_invoice(vendor_id: str, amount: float, invoice_number: str, description: str) -> Dict[str, Any]:
    """
    Process a vendor invoice for payment.
    
    Args:
        vendor_id: Vendor ID
        amount: Invoice amount
        invoice_number: Invoice number
        description: Invoice description
    
    Returns:
        dict: Invoice processing result
    """
    vendors = load_json_data("data/vendors.json") or []
    
    vendor = next((v for v in vendors if v["vendor_id"] == vendor_id), None)
    
    if not vendor:
        return {
            "status": "error",
            "message": f"Vendor {vendor_id} not found"
        }

    if amount <= 0:
        return {
            "status": "error",
            "message": "Invoice amount must be greater than 0"
        }

    if not invoice_number or not invoice_number.strip():
        return {
            "status": "error",
            "message": "Invoice number is required"
        }

    invoice_number_clean = invoice_number.strip()
    invoice_id = invoice_number_clean if invoice_number_clean.upper().startswith("INV") else f"INV{invoice_number_clean}"

    invoices = load_json_data("data/invoices.json") or []
    existing = next((inv for inv in invoices if inv.get("invoice_id") == invoice_id), None)
    if existing:
        return {
            "status": "error",
            "message": f"Invoice {invoice_id} already exists"
        }

    invoice_record = {
        "invoice_id": invoice_id,
        "invoice_number": invoice_number_clean,
        "vendor_id": vendor_id,
        "vendor_name": vendor["name"],
        "amount": amount,
        "description": description,
        "payment_terms": vendor["payment_terms"],
        "processed_at": get_timestamp(),
        "payment_status": "scheduled"
    }
    invoices.append(invoice_record)
    save_json_data("data/invoices.json", invoices)
    
    return {
        "status": "success",
        "message": f"Invoice {invoice_number_clean} processed for payment",
        **invoice_record
    }

@tool
def generate_financial_report(report_type: str, period: str) -> Dict[str, Any]:
    """
    Generate financial reports.
    
    Args:
        report_type: Type of report (expense_summary, budget_overview, vendor_spending)
        period: Report period (monthly, quarterly, yearly)
    
    Returns:
        dict: Financial report
    """
    if report_type == "expense_summary":
        return {
            "status": "success",
            "report_type": "Expense Summary",
            "period": period,
            "data": {
                "total_expenses": 1785.50,
                "approved": 450.00,
                "pending": 1335.50,
                "by_category": {
                    "travel": 1250.00,
                    "marketing": 450.00,
                    "meals": 85.50
                }
            },
            "generated_at": get_timestamp()
        }
    elif report_type == "budget_overview":
        return {
            "status": "success",
            "report_type": "Budget Overview",
            "period": period,
            "data": {
                "total_allocated": 1650000,
                "total_spent": 1400000,
                "total_remaining": 250000,
                "average_utilization": 84.8
            },
            "generated_at": get_timestamp()
        }
    else:
        return {
            "status": "error",
            "message": f"Unknown report type: {report_type}",
            "available_types": ["expense_summary", "budget_overview", "vendor_spending"]
        }
