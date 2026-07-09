from src.core import BaseAgent
from src.tools import (
    create_lead,
    update_opportunity_stage,
    get_lead_details,
    list_pipeline,
    search_customer,
)


class SalesAgent(BaseAgent):
    def __init__(self):
        system_prompt = """You are the Sales Agent, responsible for CRM and revenue operations.

Your capabilities:
1. Create and manage leads
2. Update opportunity stages
3. Retrieve lead/customer details
4. Summarize pipeline health
5. Support customer/account lookup

Be concise, commercial, and action-oriented."""

        tools = [
            create_lead,
            update_opportunity_stage,
            get_lead_details,
            list_pipeline,
            search_customer,
        ]

        super().__init__(
            name="Sales",
            role="Sales Operations Specialist",
            system_prompt=system_prompt,
            tools=tools,
            model_type="gpt35",
        )
