# 🚀 Quick Setup Guide

## Step-by-Step Installation

### 1. Prerequisites Check

Ensure you have:
- ✅ Python 3.10 or higher
- ✅ pip (Python package manager)
- ✅ OpenAI API key ([Get one here](https://platform.openai.com/api-keys))
- ✅ Internet connection

**Check Python version:**
```bash
python --version
# Should show: Python 3.10.x or higher
```

---

### 2. Navigate to Project Directory

```bash
cd c:\Jai\Work\HCL-Hackathon\AgenticWorkflows
```

---

### 3. Create Virtual Environment (Recommended)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

---

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

This will install:
- LangGraph & LangChain
- OpenAI SDK
- Streamlit
- Other required packages

**Installation takes ~2-3 minutes**

---

### 5. Configure Environment Variables

**Create .env file:**
```bash
copy .env.example .env
```

**Edit .env file and add your OpenAI API key:**
```env
OPENAI_API_KEY=sk-your-actual-api-key-here
OPENAI_MODEL_GPT4=gpt-4o-mini
OPENAI_MODEL_GPT35=gpt-3.5-turbo
TEMPERATURE_REASONING=0.7
TEMPERATURE_STRUCTURED=0.3
MAX_TOKENS=4000
```

**⚠️ Important:** Replace `sk-your-actual-api-key-here` with your real OpenAI API key!

---

### 6. Test the System

Run the test script to verify everything is working:

```bash
python test_system.py
```

**Expected output:**
```
🧪 Testing imports...
  ✅ Config module
  ✅ Core module
  ✅ Tools module
  ✅ Agents module
  ✅ Graph module

🧪 Testing data files...
  ✅ data/employees.json (5 records)
  ✅ data/tickets.json (3 records)
  ✅ data/expenses.json (3 records)
  ✅ data/vendors.json (4 records)

🧪 Testing tools...
  ✅ get_employee_info
  ✅ search_vendors

🧪 Testing intent parsing...
  ✅ 'Reset my password' → it
  ✅ 'Apply for leave' → hr
  ✅ 'Approve expense' → finance
  ✅ 'Create purchase order' → procurement

🧪 Testing configuration...
  📝 API Key: ✅ Set
  📝 GPT-4 Model: gpt-4o-mini
  📝 GPT-3.5 Model: gpt-3.5-turbo

🎉 All tests passed! System is ready to run.
```

---

### 7. Run the Application

**Option 1: Using run script (Recommended)**
```bash
python run.py
```

**Option 2: Direct Streamlit**
```bash
streamlit run app/main.py
```

**The application will:**
1. Start the Streamlit server
2. Automatically open in your browser at `http://localhost:8501`
3. Display the Enterprise Operations Hub interface

---

## 🎯 First Steps After Launch

### 1. Verify UI Loads
- Check that all agents are visible in sidebar
- Confirm API key status shows ✅ Configured

### 2. Try Quick Actions
Click any Quick Action button in the sidebar:
- 🔐 Reset Password
- 🏖️ Request Leave
- 💰 Approve Expense
- 🛒 Create Purchase Order
- 👤 Onboard Employee

### 3. Test Custom Queries
Type in the chat input:
```
"Reset my password for john.doe@company.com"
"I want to apply for 3 days leave next week"
"Show me the budget for Engineering department"
```

---

## 🐛 Troubleshooting

### Issue: "Module not found" error

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "OPENAI_API_KEY not set"

**Solution:**
1. Check `.env` file exists
2. Verify API key is correct (starts with `sk-`)
3. No spaces around the `=` sign
4. Restart the application

### Issue: "Port 8501 already in use"

**Solution:**
```bash
# Kill existing Streamlit process
# Windows:
taskkill /F /IM streamlit.exe

# Mac/Linux:
pkill -f streamlit

# Or use different port:
streamlit run app/main.py --server.port 8502
```

### Issue: Agents not responding

**Checklist:**
- ✅ API key is valid and has credits
- ✅ Internet connection is working
- ✅ OpenAI API is not down ([Check status](https://status.openai.com/))
- ✅ No firewall blocking requests

### Issue: JSON decode errors

**Solution:**
```bash
# Verify data files
python -c "import json; print(json.load(open('data/employees.json')))"
```

---

## 📊 System Requirements

### Minimum
- **CPU:** 2 cores
- **RAM:** 4 GB
- **Disk:** 500 MB free space
- **Internet:** Stable connection for API calls

### Recommended
- **CPU:** 4+ cores
- **RAM:** 8 GB
- **Disk:** 1 GB free space
- **Internet:** High-speed connection

---

## 🔐 Security Notes

### API Key Security
- ✅ Never commit `.env` file to git
- ✅ Keep API key confidential
- ✅ Use environment variables in production
- ✅ Rotate keys regularly

### Data Privacy
- Mock data is used for demo
- No real employee data in repository
- Audit logs track all actions
- Ready for GDPR compliance

---

## 📚 Next Steps

1. **Read Documentation**
   - `README.md` - Overview and features
   - `ARCHITECTURE.md` - Technical design
   - `DEMO.md` - Demo script

2. **Explore the Code**
   - `src/agents/` - Agent implementations
   - `src/tools/` - Tool definitions
   - `src/graph/` - Workflow orchestration

3. **Customize**
   - Add new agents
   - Create custom tools
   - Modify workflows
   - Integrate with real systems

4. **Deploy**
   - Set up production environment
   - Configure authentication
   - Add monitoring
   - Scale as needed

---

## 💡 Tips for Best Experience

### Performance
- Use GPT-3.5-turbo for faster responses
- Cache common queries
- Batch similar requests

### Cost Optimization
- GPT-3.5-turbo costs ~$0.01 per request
- GPT-4 costs ~$0.05 per request
- Monitor usage in OpenAI dashboard

### Development
- Use `.env` for local development
- Test with mock responses first
- Add logging for debugging
- Version control your changes

---

## 🆘 Getting Help

### Resources
- **Documentation:** See `README.md` and `ARCHITECTURE.md`
- **Demo Guide:** See `DEMO.md`
- **Test Script:** Run `python test_system.py`

### Common Commands
```bash
# Activate virtual environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install/update dependencies
pip install -r requirements.txt

# Run tests
python test_system.py

# Start application
python run.py

# Stop application
Ctrl + C
```

---

## ✅ Setup Checklist

Before demo/presentation:

- [ ] Python 3.10+ installed
- [ ] Virtual environment created and activated
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with valid API key
- [ ] Test script passes (`python test_system.py`)
- [ ] Application starts successfully
- [ ] All Quick Actions work
- [ ] Custom queries respond correctly
- [ ] No error messages in console
- [ ] Browser opens to correct URL

---

**You're all set! 🎉**

Run `python run.py` to start the application and begin exploring the Intelligent Enterprise Operations Hub!
