# ⚡ Quick Start - 3 Commands to Run

## 🚀 Get Started Now

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Set API Key
Create `.env` file:
```bash
copy .env.example .env
```

Edit `.env` and add:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

### 3️⃣ Run Application
```bash
python run.py
```

**That's it!** Browser opens automatically at http://localhost:8501

---

## 🎯 First Demo Actions

Try these in the UI:

1. **Click "🔐 Reset Password"** - See IT agent in action
2. **Click "🏖️ Request Leave"** - See HR agent work
3. **Click "💰 Approve Expense"** - See Finance agent process
4. **Type:** "Create PO for 50 laptops from Dell" - See Procurement agent

---

## 📊 What You Built

✅ **5 AI Agents** - Orchestrator, IT, HR, Finance, Procurement
✅ **20 Tools** - Specialized functions for each department
✅ **LangGraph Workflow** - Intelligent routing and orchestration
✅ **Streamlit UI** - Professional chat interface
✅ **Mock Data** - Ready-to-demo with sample data
✅ **Full Documentation** - Complete guides and architecture

---

## 🎬 Demo Flow

**For Hackathon Judges:**

1. **Show UI** - Modern, professional interface
2. **Run Scenario 1** - Password reset (30 sec)
3. **Run Scenario 2** - Leave request (45 sec)
4. **Run Scenario 3** - Expense approval (1 min)
5. **Run Scenario 4** - Purchase order (1.5 min)
6. **Explain Impact** - 40-60% productivity gain

**Total Demo Time:** 5-7 minutes

---

## 📁 Key Files

- `app/main.py` - Streamlit UI
- `src/agents/` - Agent implementations
- `src/tools/` - Tool definitions
- `src/graph/workflow.py` - LangGraph orchestration
- `data/*.json` - Mock databases

---

## 🆘 Troubleshooting

**Problem:** Module not found
```bash
pip install -r requirements.txt --upgrade
```

**Problem:** API key error
- Check `.env` file exists
- Verify key starts with `sk-`
- Restart application

**Problem:** Port in use
```bash
streamlit run app/main.py --server.port 8502
```

---

## 📚 Full Documentation

- **INSTALL_NOW.md** - 5-minute setup
- **SETUP.md** - Detailed installation
- **DEMO.md** - Complete demo script
- **ARCHITECTURE.md** - Technical design
- **PROJECT_SUMMARY.md** - What's been built

---

**Ready to impress! 🎉**
