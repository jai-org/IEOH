# ⚡ Quick Install - Start Here!

## 🚀 Get Running in 5 Minutes

### Step 1: Install Dependencies (2 minutes)

Open terminal in this directory and run:

```bash
pip install -r requirements.txt
```

**Wait for installation to complete...**

---

### Step 2: Configure API Key (1 minute)

1. **Copy the example environment file:**
```bash
copy .env.example .env
```

2. **Edit `.env` file** and add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-key-here
```

**Get API key:** https://platform.openai.com/api-keys

---

### Step 3: Test the System (1 minute)

```bash
python test_system.py
```

**Should see:** ✅ All tests passed!

---

### Step 4: Run the Application (1 minute)

```bash
python run.py
```

**Browser will open automatically to:** http://localhost:8501

---

## 🎯 Try It Out!

Once the app loads:

1. **Click a Quick Action button** in the sidebar:
   - 🔐 Reset Password
   - 🏖️ Request Leave
   - 💰 Approve Expense

2. **Or type a request:**
   - "Reset my password"
   - "Apply for 3 days leave"
   - "Approve expense EXP001"

---

## ❌ If Something Goes Wrong

### "No module named..." error
```bash
pip install -r requirements.txt --upgrade
```

### "API key not set" error
1. Check `.env` file exists
2. Verify API key starts with `sk-`
3. Restart the app

### Port already in use
```bash
streamlit run app/main.py --server.port 8502
```

---

## 📚 Full Documentation

- **Setup Guide:** `SETUP.md`
- **Architecture:** `ARCHITECTURE.md`
- **Demo Script:** `DEMO.md`
- **README:** `README.md`

---

**That's it! You're ready to go! 🎉**
