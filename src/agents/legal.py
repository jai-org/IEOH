from src.core import BaseAgent
from src.tools import (
    create_contract,
    review_contract_risk,
    check_compliance,
    get_contract_status,
    update_contract_status,
)


class LegalAgent(BaseAgent):
    def __init__(self):
        system_prompt = """You are the Legal Agent, responsible for contract lifecycle and compliance support.

Your capabilities:
1. Create contract records
2. Perform lightweight risk review
3. Provide compliance guidance
4. Track contract status
5. Update contract lifecycle stages

Be careful, explicit, and compliance-aware."""

        tools = [
            create_contract,
            review_contract_risk,
            check_compliance,
            get_contract_status,
            update_contract_status,
        ]

        super().__init__(
            name="Legal",
            role="Legal Operations Specialist",
            system_prompt=system_prompt,
            tools=tools,
            model_type="gpt4",
        )
