from langchain.tools import tool
from typing import Dict, Any
from src.core.utils import generate_po_id, get_timestamp, load_json_data, save_json_data

@tool
def search_vendors(category: str, min_rating: float = 0.0) -> Dict[str, Any]:
    """
    Search for vendors by category and rating.
    
    Args:
        category: Vendor category (IT Equipment, Office Supplies, Software & Services)
        min_rating: Minimum vendor rating (0.0 to 5.0)
    
    Returns:
        dict: List of matching vendors
    """
    vendors = load_json_data("data/vendors.json") or []
    
    matching_vendors = [
        v for v in vendors 
        if category.lower() in v["category"].lower() and v["rating"] >= min_rating
    ]
    
    if not matching_vendors:
        return {
            "status": "error",
            "message": f"No vendors found for category '{category}' with rating >= {min_rating}"
        }
    
    return {
        "status": "success",
        "category": category,
        "min_rating": min_rating,
        "vendors": matching_vendors,
        "count": len(matching_vendors)
    }

@tool
def create_purchase_order(vendor_id: str, items: str, quantity: int, estimated_cost: float, requester_id: str) -> Dict[str, Any]:
    """
    Create a purchase order for procurement.
    
    Args:
        vendor_id: Vendor ID
        items: Description of items to purchase
        quantity: Quantity of items
        estimated_cost: Estimated total cost
        requester_id: Employee ID of requester
    
    Returns:
        dict: Purchase order details
    """
    vendors = load_json_data("data/vendors.json") or []
    employees = load_json_data("data/employees.json") or []
    
    vendor = next((v for v in vendors if v["vendor_id"] == vendor_id), None)
    
    if not vendor:
        return {
            "status": "error",
            "message": f"Vendor {vendor_id} not found"
        }

    requester = next((emp for emp in employees if emp["employee_id"] == requester_id), None)
    if not requester:
        return {
            "status": "error",
            "message": f"Requester {requester_id} not found"
        }

    if quantity <= 0:
        return {
            "status": "error",
            "message": "Quantity must be greater than 0"
        }

    if estimated_cost <= 0:
        return {
            "status": "error",
            "message": "Estimated cost must be greater than 0"
        }

    if not items or not items.strip():
        return {
            "status": "error",
            "message": "Items description is required"
        }
    
    po_id = generate_po_id()
    
    approval_required = estimated_cost > 5000
    
    purchase_orders = load_json_data("data/purchase_orders.json") or []
    new_po = {
        "po_id": po_id,
        "vendor_name": vendor["name"],
        "vendor_id": vendor_id,
        "items": items,
        "quantity": quantity,
        "estimated_cost": estimated_cost,
        "requester_id": requester_id,
        "requester_name": requester["name"],
        "payment_terms": vendor["payment_terms"],
        "approval_required": approval_required,
        "po_status": "pending_approval" if approval_required else "approved",
        "created_at": get_timestamp()
    }
    purchase_orders.append(new_po)
    save_json_data("data/purchase_orders.json", purchase_orders)

    return {
        "status": "success",
        "message": f"Purchase order {po_id} created successfully",
        **new_po
    }

@tool
def check_vendor_rating(vendor_id: str) -> Dict[str, Any]:
    """
    Check vendor rating and performance metrics.
    
    Args:
        vendor_id: Vendor ID
    
    Returns:
        dict: Vendor rating and details
    """
    vendors = load_json_data("data/vendors.json") or []
    
    vendor = next((v for v in vendors if v["vendor_id"] == vendor_id), None)
    
    if not vendor:
        return {
            "status": "error",
            "message": f"Vendor {vendor_id} not found"
        }
    
    performance_metrics = {
        "on_time_delivery": 92,
        "quality_score": 88,
        "response_time": "< 24 hours",
        "contract_compliance": 95
    }
    
    return {
        "status": "success",
        "vendor": vendor,
        "performance": performance_metrics,
        "recommendation": "Approved vendor" if vendor["rating"] >= 4.0 else "Review required"
    }

@tool
def get_purchase_order_status(po_id: str) -> Dict[str, Any]:
    """
    Check status of a purchase order.
    
    Args:
        po_id: Purchase order ID
    
    Returns:
        dict: PO status details
    """
    purchase_orders = load_json_data("data/purchase_orders.json") or []
    dynamic_po = next((po for po in purchase_orders if po.get("po_id") == po_id), None)
    if dynamic_po:
        return {
            "status": "success",
            "purchase_order": dynamic_po
        }

    po_statuses = {
        "PO001": {
            "po_id": "PO001",
            "status": "delivered",
            "vendor": "TechSupply Inc",
            "items": "50 Laptops",
            "cost": 75000,
            "created_at": "2024-06-15T10:00:00Z",
            "delivered_at": "2024-06-25T14:30:00Z"
        },
        "PO002": {
            "po_id": "PO002",
            "status": "in_transit",
            "vendor": "Office Essentials Co",
            "items": "Office Furniture",
            "cost": 12000,
            "created_at": "2024-06-20T09:00:00Z",
            "expected_delivery": "2024-07-05"
        }
    }
    
    po = po_statuses.get(po_id)
    
    if not po:
        return {
            "status": "error",
            "message": f"Purchase order {po_id} not found"
        }
    
    return {
        "status": "success",
        "purchase_order": po
    }

@tool
def evaluate_vendor(vendor_name: str, criteria: str) -> Dict[str, Any]:
    """
    Evaluate a vendor based on specific criteria.
    
    Args:
        vendor_name: Name of the vendor
        criteria: Evaluation criteria (price, quality, delivery, support)
    
    Returns:
        dict: Vendor evaluation results
    """
    vendors = load_json_data("data/vendors.json") or []
    
    vendor = next((v for v in vendors if vendor_name.lower() in v["name"].lower()), None)
    
    if not vendor:
        return {
            "status": "error",
            "message": f"Vendor '{vendor_name}' not found"
        }
    
    evaluation_scores = {
        "price": 85,
        "quality": 90,
        "delivery": 88,
        "support": 92
    }
    
    criteria_lower = criteria.lower()
    score = evaluation_scores.get(criteria_lower, 0)
    
    return {
        "status": "success",
        "vendor_name": vendor["name"],
        "vendor_id": vendor["vendor_id"],
        "criteria": criteria,
        "score": score,
        "overall_rating": vendor["rating"],
        "recommendation": "Highly recommended" if score >= 85 else "Acceptable" if score >= 70 else "Review alternatives"
    }
