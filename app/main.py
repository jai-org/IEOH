import streamlit as st
import sys
import os
import html
from datetime import datetime
import uuid
import pandas as pd
import plotly.express as px

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.graph import app as workflow_app
from src.core import (
    generate_session_id,
    get_pending_approvals,
    decide_approval,
    get_recent_workflow_runs,
    persist_workflow_execution,
)
from src.config import settings

st.set_page_config(
    page_title="Enterprise Operations Hub",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .agent-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 1rem;
        font-size: 0.875rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    .agent-orchestrator { background-color: #e3f2fd; color: #1976d2; }
    .agent-it { background-color: #f3e5f5; color: #7b1fa2; }
    .agent-hr { background-color: #e8f5e9; color: #388e3c; }
    .agent-finance { background-color: #fff3e0; color: #f57c00; }
    .agent-procurement { background-color: #fce4ec; color: #c2185b; }
    .agent-sales { background-color: #e8eaf6; color: #3949ab; }
    .agent-marketing { background-color: #fff8e1; color: #ef6c00; }
    .agent-legal { background-color: #eceff1; color: #455a64; }
    .status-success { color: #4caf50; font-weight: bold; }
    .status-error { color: #f44336; font-weight: bold; }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        border-left: 4px solid;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left-color: #2196f3;
    }
    .agent-message {
        background-color: #f5f5f5;
        border-left-color: #9e9e9e;
    }
</style>
""", unsafe_allow_html=True)

if "session_id" not in st.session_state:
    st.session_state.session_id = generate_session_id()
if "messages" not in st.session_state:
    st.session_state.messages = []
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "last_execution" not in st.session_state:
    st.session_state.last_execution = None
if "approver_id" not in st.session_state:
    st.session_state.approver_id = "security.reviewer@company.com"

st.markdown('<div class="main-header">🏢 Intelligent Enterprise Operations Hub</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">AI-Powered Multi-Agent System for Enterprise Automation</div>', unsafe_allow_html=True)

with st.sidebar:
    st.header("🎯 Quick Actions")
    
    if st.button("🔐 Reset Password", use_container_width=True):
        st.session_state.quick_action = "I need to reset my password for john.doe@company.com"
    
    if st.button("🏖️ Request Leave", use_container_width=True):
        st.session_state.quick_action = "I want to apply for 3 days leave from 2024-07-15 to 2024-07-17"
    
    if st.button("💰 Approve Expense", use_container_width=True):
        st.session_state.quick_action = "Approve expense report EXP001"
    
    if st.button("🛒 Create Purchase Order", use_container_width=True):
        st.session_state.quick_action = "Create purchase order for 50 laptops from Dell"
    
    if st.button("👤 Onboard Employee", use_container_width=True):
        st.session_state.quick_action = "Onboard new employee Sarah Johnson in Engineering as Senior Developer starting 2024-07-01, manager EMP050"
    if st.button("🏗️ Enterprise Onboarding Workflow", use_container_width=True):
        st.session_state.quick_action = (
            "Onboard Sachin Sharma as a Data Analyst in Hyderabad starting July 15. "
            "He needs Gmail, Jenkins, Jira, GitHub, and VS Code. "
            "Laptop preference: MacBook Air. Manager: Rahul Mehta."
        )

    if st.button("📈 Create Sales Lead", use_container_width=True):
        st.session_state.quick_action = "Create a new lead for Alex Carter at Acme Corp, email alex@acme.com, source LinkedIn"

    if st.button("📣 Launch Campaign", use_container_width=True):
        st.session_state.quick_action = "Create a marketing campaign named Q3 Product Push on LinkedIn with budget 10000 for lead generation"

    if st.button("⚖️ Review Contract", use_container_width=True):
        st.session_state.quick_action = "Create a contract named Data Processing Agreement with Beta Inc, type DPA, owner EMP004 and review risk"
    
    st.divider()
    
    st.header("🤖 Active Agents")
    st.markdown('<span class="agent-badge agent-orchestrator">🎯 Orchestrator</span>', unsafe_allow_html=True)
    st.markdown('<span class="agent-badge agent-it">🔧 IT Support</span>', unsafe_allow_html=True)
    st.markdown('<span class="agent-badge agent-hr">👥 HR Operations</span>', unsafe_allow_html=True)
    st.markdown('<span class="agent-badge agent-finance">💰 Finance</span>', unsafe_allow_html=True)
    st.markdown('<span class="agent-badge agent-procurement">🛒 Procurement</span>', unsafe_allow_html=True)
    st.markdown('<span class="agent-badge agent-sales">📈 Sales</span>', unsafe_allow_html=True)
    st.markdown('<span class="agent-badge agent-marketing">📣 Marketing</span>', unsafe_allow_html=True)
    st.markdown('<span class="agent-badge agent-legal">⚖️ Legal</span>', unsafe_allow_html=True)
    
    st.divider()
    
    st.header("📊 Session Info")
    st.text(f"Session: {st.session_state.session_id[:8]}...")
    st.text(f"Messages: {len(st.session_state.messages)}")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.conversation_history = []
        st.session_state.last_execution = None
        st.rerun()
    
    st.divider()
    
    st.header("⚙️ Settings")
    api_key_status = "✅ Configured" if settings.OPENAI_API_KEY else "❌ Not Set"
    st.text(f"API Key: {api_key_status}")
    st.text(f"Model: {settings.OPENAI_MODEL_GPT4}")
    
    if not settings.OPENAI_API_KEY:
        st.warning("⚠️ Please set OPENAI_API_KEY in .env file")

    st.divider()
    st.header("🛡️ Approval Controls")
    st.session_state.approver_id = st.text_input(
        "Approver Identity",
        value=st.session_state.approver_id,
        help="Used for approval audit entries.",
    )

for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    safe_content = html.escape(str(content)).replace("\n", "<br>")
    
    if role == "user":
        st.markdown(f'<div class="chat-message user-message"><strong>👤 You:</strong><br>{safe_content}</div>', unsafe_allow_html=True)
    else:
        agent_name = message.get("agent", "Assistant")
        safe_agent_name = html.escape(str(agent_name))
        st.markdown(f'<div class="chat-message agent-message"><strong>🤖 {safe_agent_name}:</strong><br>{safe_content}</div>', unsafe_allow_html=True)

typed_input = st.chat_input("Type your request here... (e.g., 'Reset my password', 'Apply for leave', 'Approve expense EXP001')")
quick_action_input = st.session_state.pop("quick_action", None) if "quick_action" in st.session_state else None
user_input = quick_action_input or typed_input

if user_input:
    if not settings.OPENAI_API_KEY:
        st.error("❌ Please configure your OpenAI API key in the .env file to use the agents.")
        st.stop()
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    safe_user_input = html.escape(str(user_input)).replace("\n", "<br>")
    st.markdown(f'<div class="chat-message user-message"><strong>👤 You:</strong><br>{safe_user_input}</div>', unsafe_allow_html=True)
    
    with st.spinner("🤖 Agents are processing your request..."):
        try:
            initial_state = {
                "user_request": user_input,
                "user_id": "EMP001",
                "department": None,
                "target_agent": "",
                "workflow_type": "",
                "priority": "medium",
                "current_agent": "",
                "messages": [],
                "agent_responses": [],
                "tool_calls": [],
                "conversation_history": st.session_state.conversation_history,
                "session_id": st.session_state.session_id,
                "metadata": {},
                "final_response": "",
                "status": "",
                "next_steps": []
            }
            
            result = workflow_app.invoke(initial_state)
            execution_dashboard = result.get("metadata", {}).get("execution_dashboard")
            st.session_state.last_execution = execution_dashboard
            
            final_response = result.get("final_response", "Request processed successfully.")
            agent_responses = result.get("agent_responses", [])
            
            response_text = ""
            for resp in agent_responses:
                agent_name = resp.get("agent", "Agent")
                if "message" in resp:
                    response_text += f"**{agent_name}:** {resp['message']}\n\n"
                elif "response" in resp:
                    response_text += f"**{agent_name}:** {resp['response']}\n\n"
            
            if not response_text:
                response_text = final_response

            # Persist non-enterprise runs too, so analytics charts evolve with all requests.
            if not execution_dashboard:
                synthetic_run_id = f"RUN-{uuid.uuid4().hex[:10].upper()}"
                synthetic_dashboard = {
                    "run_id": synthetic_run_id,
                    "request_type": result.get("workflow_type", "general"),
                    "tasks": [
                        {
                            "task_id": "T001",
                            "department": result.get("current_agent", "orchestrator"),
                            "agent": result.get("current_agent", "System"),
                            "task": "Handle user request",
                            "status": "success" if result.get("status") != "error" else "error",
                            "detail": final_response,
                            "timestamp": datetime.now().isoformat(),
                        }
                    ],
                    "approvals_pending": [],
                    "documents": [],
                    "emails": [],
                    "audit_trail": [
                        {
                            "timestamp": datetime.now().isoformat(),
                            "event": "WorkflowCompleted",
                            "detail": f"Processed request with status {result.get('status', 'completed')}",
                        }
                    ],
                    "metrics": {
                        "total_tasks": 1,
                        "completed_tasks": 1 if result.get("status") != "error" else 0,
                        "pending_approvals": 0,
                        "automation_rate_percent": 100.0 if result.get("status") != "error" else 0.0,
                        "estimated_manual_minutes_saved": 10 if result.get("status") != "error" else 0,
                    },
                }
                persist_workflow_execution(
                    run_id=synthetic_run_id,
                    session_id=st.session_state.session_id,
                    request_text=user_input,
                    workflow_type=str(result.get("workflow_type", "general")),
                    status=str(result.get("status", "completed")),
                    execution_dashboard=synthetic_dashboard,
                )
            
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text,
                "agent": result.get("current_agent", "System")
            })
            
            st.session_state.conversation_history.append({
                "role": "user",
                "content": user_input
            })
            st.session_state.conversation_history.append({
                "role": "assistant",
                "content": response_text
            })
            
            safe_agent = html.escape(str(result.get("current_agent", "System").title()))
            safe_response = html.escape(str(response_text)).replace("\n", "<br>")
            st.markdown(f'<div class="chat-message agent-message"><strong>🤖 {safe_agent}:</strong><br>{safe_response}</div>', unsafe_allow_html=True)
            
            if result.get("status") == "completed":
                st.success("✅ Request completed successfully!")
            elif result.get("status") == "pending_approval":
                st.warning("⏸️ Workflow paused: human approval required for risky actions.")
            elif result.get("status") == "error":
                st.error("❌ An error occurred while processing your request.")
            
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            st.error(f"❌ {error_message}")
            st.session_state.messages.append({
                "role": "assistant",
                "content": error_message,
                "agent": "System"
            })

if len(st.session_state.messages) == 0:
    st.info("👋 Welcome! I'm your Enterprise Operations Hub assistant. Try asking me to:\n\n"
            "- Reset a password\n"
            "- Request leave\n"
            "- Approve an expense\n"
            "- Create a purchase order\n"
            "- Onboard a new employee\n"
            "- Create a sales lead\n"
            "- Launch a marketing campaign\n"
            "- Review a contract or compliance topic\n\n"
            "Or click a Quick Action button in the sidebar!")

execution = st.session_state.get("last_execution")
if execution:
    st.divider()
    st.subheader("📈 Live Execution Dashboard")

    metrics = execution.get("metrics", {})
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tasks", metrics.get("total_tasks", 0))
    col2.metric("Completed", metrics.get("completed_tasks", 0))
    col3.metric("Pending Approvals", metrics.get("pending_approvals", 0))
    col4.metric("Minutes Saved", metrics.get("estimated_manual_minutes_saved", 0))

    st.markdown("#### Task Execution")
    st.dataframe(execution.get("tasks", []), use_container_width=True)

    approvals = execution.get("approvals_pending", [])
    if approvals:
        st.markdown("#### Approval Queue")
        st.warning("Risky actions are paused until approved by a human reviewer.")
        st.dataframe(approvals, use_container_width=True)

    st.markdown("#### Generated Documents")
    for doc in execution.get("documents", []):
        with st.expander(f"{doc.get('title', 'Document')} ({doc.get('type', 'doc')})"):
            st.code(doc.get("content", ""), language="text")

    st.markdown("#### Email Drafts")
    for email in execution.get("emails", []):
        with st.expander(f"To: {email.get('to', 'unknown')} | {email.get('subject', '')}"):
            st.write(email.get("body", ""))

    st.markdown("#### Audit Trail")
    st.dataframe(execution.get("audit_trail", []), use_container_width=True)

st.divider()
st.subheader("🏢 Enterprise Operations Center")

pending = get_pending_approvals(limit=30)
if pending:
    st.markdown("#### Pending Approvals")
    pending_df = pd.DataFrame(pending)
    st.dataframe(pending_df, use_container_width=True)

    selected_approval = st.selectbox(
        "Select Approval ID",
        options=[p["approval_id"] for p in pending],
        key="approval_select",
    )
    selected_detail = next((p for p in pending if p["approval_id"] == selected_approval), None)
    if selected_detail:
        st.info(
            f"{selected_detail['department']} | {selected_detail['action']} | Reason: {selected_detail['reason']}"
        )
        col_a, col_b = st.columns(2)
        if col_a.button("✅ Approve Selected", use_container_width=True):
            if decide_approval(selected_approval, "approved", st.session_state.approver_id):
                st.success(f"Approval {selected_approval} approved.")
                st.rerun()
            st.error("Unable to approve selection.")
        if col_b.button("❌ Reject Selected", use_container_width=True):
            if decide_approval(selected_approval, "rejected", st.session_state.approver_id):
                st.success(f"Approval {selected_approval} rejected.")
                st.rerun()
            st.error("Unable to reject selection.")
else:
    st.success("No pending approvals in the enterprise queue.")

runs = get_recent_workflow_runs(limit=50)
if runs:
    runs_df = pd.DataFrame(runs)
    runs_df["created_at"] = pd.to_datetime(runs_df["created_at"])
    runs_df["run_seq"] = range(1, len(runs_df) + 1)

    st.markdown("#### Workflow Analytics")
    analytics_limit = st.slider(
        "Runs to visualize",
        min_value=10,
        max_value=200,
        value=50,
        step=10,
    )
    runs_view = runs_df.sort_values("created_at").tail(analytics_limit)
    col_left, col_right = st.columns(2)

    workflow_counts = runs_view["workflow_type"].value_counts().reset_index()
    workflow_counts.columns = ["workflow_type", "count"]
    workflow_fig = px.bar(
        workflow_counts,
        x="workflow_type",
        y="count",
        title="Runs by Workflow Type",
        color="workflow_type",
    )
    col_left.plotly_chart(workflow_fig, use_container_width=True)

    trend_long = runs_view.melt(
        id_vars=["created_at", "run_id"],
        value_vars=["automation_rate_percent", "estimated_manual_minutes_saved"],
        var_name="metric",
        value_name="value",
    )
    trend_fig = px.line(
        trend_long,
        x="created_at",
        y="value",
        color="metric",
        markers=True,
        title="Automation & Productivity Trend",
        hover_data=["run_id"],
    )
    col_right.plotly_chart(trend_fig, use_container_width=True)

    st.dataframe(
        runs_view[
            [
                "run_id",
                "workflow_type",
                "status",
                "automation_rate_percent",
                "estimated_manual_minutes_saved",
                "created_at",
            ]
        ],
        use_container_width=True,
    )
else:
    st.info("No workflow runs captured yet. Trigger an onboarding workflow to populate analytics.")
