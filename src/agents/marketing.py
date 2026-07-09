from src.core import BaseAgent
from src.tools import (
    create_campaign,
    update_campaign_status,
    get_campaign_performance,
    list_active_campaigns,
    recommend_channel,
)


class MarketingAgent(BaseAgent):
    def __init__(self):
        system_prompt = """You are the Marketing Agent, responsible for campaign planning and optimization.

Your capabilities:
1. Create and manage campaigns
2. Update campaign status
3. Report campaign performance
4. Track active campaigns
5. Recommend channels by audience and objective

Be structured, measurable, and growth-focused."""

        tools = [
            create_campaign,
            update_campaign_status,
            get_campaign_performance,
            list_active_campaigns,
            recommend_channel,
        ]

        super().__init__(
            name="Marketing",
            role="Marketing Operations Specialist",
            system_prompt=system_prompt,
            tools=tools,
            model_type="gpt35",
        )
