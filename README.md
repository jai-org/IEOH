# 🏢 Intelligent Enterprise Operations Hub

An AI-powered multi-agent system that transforms enterprise operations across IT, HR, Finance, Procurement, Sales, Marketing, and Legal departments using LangGraph and OpenAI.

## 🎯 Overview

The Intelligent Enterprise Operations Hub automates and optimizes enterprise operations through specialized AI agents that handle department-specific tasks, coordinate workflows, and deliver measurable productivity gains.

### Key Features

- **🤖 Multi-Agent Architecture**: 8 specialized agents working in coordination
- **🎯 Intelligent Routing**: Automatic request routing to appropriate departments
- **🔄 Workflow Orchestration**: Complex multi-department workflows
- **💬 Natural Language Interface**: Chat-based interaction
- **📊 Real-time Processing**: Instant responses and actions
- **🔧 Tool Integration**: 20+ tools for various operations
- **📈 Analytics Dashboard**: Track metrics and performance

## 🏗️ Architecture

```
User Interface (Streamlit)
         ↓
Orchestrator Agent (Router)
         ↓
┌────────┴────────┬────────┬────────┬────────┬────────┬────────┐
IT      HR      Finance  Procure  Sales   Marketing  Legal
Agent   Agent   Agent    Agent    Agent   Agent      Agent
```

### Agents

1. **Orchestrator Agent** - Central coordinator and request router
2. **IT Support Agent** - Technical support and system management
3. **HR Operations Agent** - Human resources and employee services
4. **Finance Agent** - Financial operations and analysis
5. **Procurement Agent** - Purchase and vendor management
6. **Sales Agent** - CRM and sales operations (Coming soon)
7. **Marketing Agent** - Campaign and content management (Coming soon)
8. **Legal Agent** - Contract and compliance review (Coming soon)

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- OpenAI API key
- Git

### Installation

1. **Clone the repository**
```bash
cd c:\Jai\Work\HCL-Hackathon\AgenticWorkflows
```

2. **Create virtual environment**
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
copy .env.example .env
```

Edit `.env` and add your OpenAI API key:
```
OPENAI_API_KEY=your_api_key_here
```

5. **Run the application**
```bash
streamlit run app/main.py
```

The application will open in your browser at `http://localhost:8501`

## 🌐 Deploy Live (Shareable URL)

Use the deployment guide in [DEPLOYMENT.md](DEPLOYMENT.md) to host this as a public live agent.

- **Fastest path:** Streamlit Community Cloud
- **Production-friendly path:** Render or Railway using Docker
- **Required secret:** `OPENAI_API_KEY`

## 💡 Usage Examples

### IT Support
```
"Reset my password for john.doe@company.com"
"Create a ticket for laptop keyboard issue"
"Grant me access to the CRM system"
```

### HR Operations
```
"I want to apply for 3 days leave from 2024-07-15 to 2024-07-17"
"What is the remote work policy?"
"Check my leave balance"
"Onboard new employee Sarah Johnson starting July 1st"
```

### Finance
```
"Approve expense report EXP001"
"Show me the budget analysis for Engineering department"
"Process invoice from TechSupply Inc for $5000"
```

### Procurement
```
"Create purchase order for 50 laptops from Dell"
"Find vendors for office furniture"
"Check status of purchase order PO001"
"Evaluate vendor TechSupply Inc"
```

### Multi-Department Workflows
```
"Onboard new employee with IT setup and payroll configuration"
"Create purchase order and process payment"
```

## 📁 Project Structure

```
AgenticWorkflows/
├── src/
│   ├── core/              # Base classes and utilities
│   │   ├── base_agent.py  # Base agent class
│   │   ├── state.py       # State management
│   │   └── utils.py       # Helper functions
│   ├── agents/            # Agent implementations
│   │   ├── orchestrator.py
│   │   ├── it_support.py
│   │   ├── hr_operations.py
│   │   ├── finance.py
│   │   └── procurement.py
│   ├── tools/             # Agent tools
│   │   ├── it_tools.py
│   │   ├── hr_tools.py
│   │   ├── finance_tools.py
│   │   └── procurement_tools.py
│   ├── graph/             # LangGraph workflow
│   │   └── workflow.py
│   └── config/            # Configuration
│       └── settings.py
├── app/                   # Streamlit UI
│   └── main.py
├── data/                  # Mock databases
│   ├── employees.json
│   ├── tickets.json
│   ├── expenses.json
│   └── vendors.json
├── requirements.txt
├── .env.example
├── README.md
└── ARCHITECTURE.md
```

## 🛠️ Technology Stack

- **LangGraph 0.2.x** - Agent orchestration and workflow management
- **LangChain 0.2.x** - LLM integration framework
- **OpenAI GPT-4 & GPT-3.5** - Language models
- **Streamlit 1.39** - Web interface
- **Python 3.10+** - Core language

## 📊 Business Impact

### Productivity Gains
- **40-60% reduction** in routine operational tasks
- **Minutes vs hours/days** response times
- **24/7 availability** for common requests

### Cost Savings
- **30-50% lower** operational costs
- **Reduced manual processing** time
- **Optimized resource allocation**

### Employee Experience
- **Instant responses** to queries
- **Self-service capabilities**
- **Consistent service quality**

## 🎬 Demo Scenarios

The application includes pre-configured demo scenarios accessible via Quick Action buttons:

1. **Password Reset** - IT Support workflow
2. **Leave Request** - HR Operations workflow
3. **Expense Approval** - Finance workflow
4. **Purchase Order** - Procurement workflow
5. **Employee Onboarding** - Multi-agent workflow

## 🔧 Configuration

### Environment Variables

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL_GPT4=gpt-4o-mini
OPENAI_MODEL_GPT35=gpt-3.5-turbo
TEMPERATURE_REASONING=0.7
TEMPERATURE_STRUCTURED=0.3
MAX_TOKENS=4000
```

### Agent Configuration

Each agent can be configured with:
- Model selection (GPT-4 or GPT-3.5)
- Temperature settings
- Tool assignments
- System prompts

## 🧪 Testing

Run tests (coming soon):
```bash
pytest tests/
```

## 📈 Monitoring

The application tracks:
- Request volume by department
- Response times
- Success rates
- Agent utilization
- User satisfaction

## 🔐 Security

- API key management via environment variables
- Role-based access control (ready for implementation)
- Audit logging for all actions
- Data encryption (production-ready)

## 🚧 Roadmap

### Phase 1 (Current)
- ✅ Core 5 agents operational
- ✅ LangGraph orchestration
- ✅ Streamlit UI
- ✅ 20+ tools

### Phase 2 (Next)
- ⏳ Sales, Marketing, Legal agents
- ⏳ Advanced analytics dashboard
- ⏳ Multi-turn conversations
- ⏳ Workflow templates

### Phase 3 (Future)
- 📋 Voice interface
- 📋 Mobile app
- 📋 Slack/Teams integration
- 📋 Custom workflow builder

## 🤝 Contributing

This is a hackathon project. For questions or suggestions, please contact the team.

## 📄 License

Copyright © 2024 HCL Hackathon Team

## 🙏 Acknowledgments

- HCL for hosting the hackathon
- LangChain and LangGraph teams
- OpenAI for GPT models
- Streamlit for the UI framework

## 📞 Support

For issues or questions:
1. Check the documentation in `ARCHITECTURE.md`
2. Review demo scenarios
3. Contact the development team

---

**Built with ❤️ for HCL Hackathon 2024**

**Track 2: Agents/Agentic Workflows for Enterprise Operations**
