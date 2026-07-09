from langchain.tools import tool
from typing import Dict, Any
from src.core.utils import get_timestamp, load_json_data, save_json_data


@tool
def create_campaign(name: str, channel: str, budget: float, objective: str) -> Dict[str, Any]:
    """Create a marketing campaign."""
    if not name.strip() or not channel.strip() or not objective.strip():
        return {"status": "error", "message": "name, channel, and objective are required"}
    if budget <= 0:
        return {"status": "error", "message": "budget must be greater than 0"}

    campaigns = load_json_data("data/campaigns.json") or []
    campaign_id = f"CMP{len(campaigns) + 1:03d}"
    campaign = {
        "campaign_id": campaign_id,
        "name": name.strip(),
        "channel": channel.strip(),
        "budget": budget,
        "objective": objective.strip(),
        "status": "planned",
        "created_at": get_timestamp(),
    }
    campaigns.append(campaign)
    save_json_data("data/campaigns.json", campaigns)
    return {"status": "success", "message": f"Campaign {campaign_id} created", "campaign": campaign}


@tool
def update_campaign_status(campaign_id: str, status: str) -> Dict[str, Any]:
    """Update campaign execution status."""
    allowed = {"planned", "active", "paused", "completed"}
    status_normalized = status.lower().strip()
    if status_normalized not in allowed:
        return {"status": "error", "message": f"Invalid status. Allowed: {', '.join(sorted(allowed))}"}

    campaigns = load_json_data("data/campaigns.json") or []
    campaign = next((c for c in campaigns if c.get("campaign_id") == campaign_id), None)
    if not campaign:
        return {"status": "error", "message": f"Campaign {campaign_id} not found"}

    campaign["status"] = status_normalized
    campaign["updated_at"] = get_timestamp()
    save_json_data("data/campaigns.json", campaigns)
    return {"status": "success", "message": f"Campaign {campaign_id} updated", "campaign": campaign}


@tool
def get_campaign_performance(campaign_id: str) -> Dict[str, Any]:
    """Return mock campaign metrics for a campaign."""
    campaigns = load_json_data("data/campaigns.json") or []
    campaign = next((c for c in campaigns if c.get("campaign_id") == campaign_id), None)
    if not campaign:
        return {"status": "error", "message": f"Campaign {campaign_id} not found"}

    performance = {
        "impressions": 15000,
        "clicks": 920,
        "conversions": 84,
        "ctr_percent": 6.13,
        "conversion_rate_percent": 9.13,
    }
    return {"status": "success", "campaign_id": campaign_id, "performance": performance}


@tool
def list_active_campaigns() -> Dict[str, Any]:
    """List active campaigns."""
    campaigns = load_json_data("data/campaigns.json") or []
    active = [c for c in campaigns if c.get("status") == "active"]
    return {"status": "success", "count": len(active), "campaigns": active}


@tool
def recommend_channel(audience: str, objective: str) -> Dict[str, Any]:
    """Recommend marketing channels based on audience/objective."""
    audience_l = audience.lower()
    objective_l = objective.lower()

    if "enterprise" in audience_l or "b2b" in audience_l:
        channels = ["LinkedIn", "Webinars", "Email"]
    elif "consumer" in audience_l or "b2c" in audience_l:
        channels = ["Instagram", "YouTube", "Search Ads"]
    else:
        channels = ["Email", "Search Ads", "Content Marketing"]

    if "brand" in objective_l:
        channels = channels[:2] + ["PR"]

    return {"status": "success", "recommended_channels": channels}
