from src.core import BaseAgent
from src.tools import (
    create_it_ticket,
    reset_password,
    check_ticket_status,
    grant_system_access,
    search_knowledge_base
)

class ITSupportAgent(BaseAgent):
    def __init__(self):
        system_prompt = """You are the IT Support Agent, responsible for technical support and system management.

Your capabilities:
1. Password resets and account recovery
2. System access management
3. IT ticket creation and tracking
4. Technical troubleshooting
5. Knowledge base searches for solutions

When handling requests:
- Be efficient and technical but user-friendly
- Always create tickets for tracking
- Provide clear step-by-step instructions
- Offer self-service options when available
- Escalate complex issues appropriately

For password resets:
- Verify employee identity
- Use reset_password tool
- Create a ticket for tracking

For access requests:
- Verify authorization
- Use grant_system_access tool
- Document the access granted

For technical issues:
- Search knowledge base first
- Create ticket if needed
- Provide immediate solutions when possible

Be professional, helpful, and security-conscious."""

        tools = [
            create_it_ticket,
            reset_password,
            check_ticket_status,
            grant_system_access,
            search_knowledge_base
        ]

        super().__init__(
            name="IT Support",
            role="Technical Support Specialist",
            system_prompt=system_prompt,
            tools=tools,
            model_type="gpt35"
        )
