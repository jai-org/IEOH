from typing import Dict, Any
from src.core import BaseAgent, parse_user_intent

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        system_prompt = """You are the Orchestrator Agent, the central coordinator of the Enterprise Operations Hub.

Your responsibilities:
1. Analyze incoming user requests
2. Determine which specialist agent(s) should handle the request
3. Route requests to the appropriate agent(s)
4. Coordinate multi-agent workflows when needed
5. Provide clear, helpful responses to users

Available specialist agents:
- IT Support Agent: Password resets, system access, technical issues, tickets
- HR Operations Agent: Leave requests, employee info, policies, onboarding
- Finance Agent: Expense approvals, budget analysis, invoices, financial reports
- Procurement Agent: Purchase orders, vendor management, procurement requests
- Sales Agent: CRM, leads, opportunities, customer management
- Marketing Agent: Campaigns, content, analytics, marketing operations
- Legal Agent: Contracts, compliance, legal review, risk assessment

When analyzing a request:
1. Identify the primary department/agent needed
2. Determine if multiple agents are required
3. Extract key information (employee IDs, dates, amounts, etc.)
4. Route to the appropriate agent with clear instructions

Be concise, professional, and helpful. Always acknowledge the user's request and explain what action will be taken."""

        super().__init__(
            name="Orchestrator",
            role="Central Coordinator",
            system_prompt=system_prompt,
            tools=[],
            model_type="gpt4"
        )
    
    def route_request(self, state: Dict[str, Any]) -> str:
        """Determine which agent should handle the request"""
        user_request = state.get("user_request", "")
        
        intent = parse_user_intent(user_request)
        primary_dept = intent.get("primary_department", "general")
        
        routing_map = {
            "it": "it_support",
            "hr": "hr_operations",
            "finance": "finance",
            "procurement": "procurement",
            "sales": "sales",
            "marketing": "marketing",
            "legal": "legal",
            "general": "orchestrator"
        }
        
        return routing_map.get(primary_dept, "orchestrator")
