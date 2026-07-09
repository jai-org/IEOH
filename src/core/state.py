from typing import TypedDict, List, Dict, Optional, Annotated
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    user_request: str
    user_id: str
    department: Optional[str]
    
    target_agent: str
    workflow_type: str
    priority: str
    
    current_agent: str
    messages: Annotated[List[Dict], add_messages]
    agent_responses: List[Dict]
    tool_calls: List[Dict]
    
    conversation_history: List[Dict]
    session_id: str
    metadata: Dict
    
    final_response: str
    status: str
    next_steps: List[str]
