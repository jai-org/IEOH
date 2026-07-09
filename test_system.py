import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from src.config import settings
        print("  ✅ Config module")
    except Exception as e:
        print(f"  ❌ Config module: {e}")
        return False
    
    try:
        from src.core import BaseAgent, AgentState, parse_user_intent, get_pending_approvals, get_recent_workflow_runs
        print("  ✅ Core module")
    except Exception as e:
        print(f"  ❌ Core module: {e}")
        return False
    
    try:
        from src.tools import (
            create_it_ticket, reset_password,
            request_leave, get_employee_info,
            approve_expense, analyze_budget,
            search_vendors, create_purchase_order,
            create_lead, create_campaign, create_contract
        )
        print("  ✅ Tools module")
    except Exception as e:
        print(f"  ❌ Tools module: {e}")
        return False
    
    try:
        from src.agents import (
            OrchestratorAgent, ITSupportAgent,
            HROperationsAgent, FinanceAgent, ProcurementAgent,
            SalesAgent, MarketingAgent, LegalAgent
        )
        print("  ✅ Agents module")
    except Exception as e:
        print(f"  ❌ Agents module: {e}")
        return False
    
    try:
        from src.graph import app, build_workflow
        print("  ✅ Graph module")
    except Exception as e:
        print(f"  ❌ Graph module: {e}")
        return False
    
    return True

def test_data_files():
    """Test if data files exist and are valid"""
    print("\n🧪 Testing data files...")
    
    data_files = [
        "data/employees.json",
        "data/tickets.json",
        "data/expenses.json",
        "data/vendors.json",
        "data/leads.json",
        "data/campaigns.json",
        "data/contracts.json"
    ]
    
    import json
    all_valid = True
    
    for filepath in data_files:
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                print(f"  ✅ {filepath} ({len(data)} records)")
            except json.JSONDecodeError:
                print(f"  ❌ {filepath} - Invalid JSON")
                all_valid = False
        else:
            print(f"  ❌ {filepath} - Not found")
            all_valid = False
    
    return all_valid

def test_tools():
    """Test if tools work correctly"""
    print("\n🧪 Testing tools...")
    
    try:
        from src.tools import get_employee_info, search_vendors, list_pipeline, list_active_campaigns, check_compliance
        
        result = get_employee_info.invoke({"employee_id": "EMP001"})
        if result.get("status") == "success":
            print("  ✅ get_employee_info")
        else:
            print("  ❌ get_employee_info")
            return False
        
        result = search_vendors.invoke({"category": "IT Equipment", "min_rating": 4.0})
        if result.get("status") == "success":
            print("  ✅ search_vendors")
        else:
            print("  ❌ search_vendors")
            return False

        result = list_pipeline.invoke({})
        if result.get("status") == "success":
            print("  ✅ list_pipeline")
        else:
            print("  ❌ list_pipeline")
            return False

        result = list_active_campaigns.invoke({})
        if result.get("status") == "success":
            print("  ✅ list_active_campaigns")
        else:
            print("  ❌ list_active_campaigns")
            return False

        result = check_compliance.invoke({"topic": "privacy"})
        if result.get("status") == "success":
            print("  ✅ check_compliance")
        else:
            print("  ❌ check_compliance")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Tool execution error: {e}")
        return False

def test_intent_parsing():
    """Test intent parsing"""
    print("\n🧪 Testing intent parsing...")
    
    try:
        from src.core import parse_user_intent
        
        test_cases = [
            ("Reset my password", "it"),
            ("Apply for leave", "hr"),
            ("Approve expense", "finance"),
            ("Create purchase order", "procurement"),
            ("Create a new lead in CRM", "sales"),
            ("Launch a new marketing campaign", "marketing"),
            ("Review this contract for compliance", "legal")
        ]
        
        for query, expected_dept in test_cases:
            result = parse_user_intent(query)
            if result["primary_department"] == expected_dept:
                print(f"  ✅ '{query}' → {expected_dept}")
            else:
                print(f"  ❌ '{query}' → {result['primary_department']} (expected {expected_dept})")
                return False
        
        return True
    except Exception as e:
        print(f"  ❌ Intent parsing error: {e}")
        return False

def test_config():
    """Test configuration"""
    print("\n🧪 Testing configuration...")
    
    try:
        from src.config import settings
        
        print(f"  📝 API Key: {'✅ Set' if settings.OPENAI_API_KEY else '❌ Not set'}")
        print(f"  📝 GPT-4 Model: {settings.OPENAI_MODEL_GPT4}")
        print(f"  📝 GPT-3.5 Model: {settings.OPENAI_MODEL_GPT35}")
        
        if not settings.OPENAI_API_KEY:
            print("  ⚠️  Warning: OPENAI_API_KEY not set in .env")
            print("  ℹ️  The system will work but agents won't be able to respond")
        
        return True
    except Exception as e:
        print(f"  ❌ Configuration error: {e}")
        return False

def test_enterprise_store():
    """Test enterprise persistence services."""
    print("\n🧪 Testing enterprise persistence...")

    try:
        from src.core import get_pending_approvals, get_recent_workflow_runs

        pending = get_pending_approvals(limit=5)
        if isinstance(pending, list):
            print("  ✅ get_pending_approvals")
        else:
            print("  ❌ get_pending_approvals")
            return False

        runs = get_recent_workflow_runs(limit=5)
        if isinstance(runs, list):
            print("  ✅ get_recent_workflow_runs")
        else:
            print("  ❌ get_recent_workflow_runs")
            return False

        return True
    except Exception as e:
        print(f"  ❌ Enterprise persistence error: {e}")
        return False

def test_enterprise_onboarding_workflow():
    """Test structured enterprise onboarding orchestration path."""
    print("\n🧪 Testing enterprise onboarding workflow...")

    try:
        from src.graph import app

        request = (
            "Onboard Sachin Sharma as a Data Analyst in Hyderabad starting July 15. "
            "He needs Gmail, Jenkins, Jira, GitHub, and VS Code. "
            "Laptop preference: MacBook Air. Manager: Rahul Mehta."
        )

        initial_state = {
            "user_request": request,
            "user_id": "EMP001",
            "department": None,
            "target_agent": "",
            "workflow_type": "",
            "priority": "high",
            "current_agent": "",
            "messages": [],
            "agent_responses": [],
            "tool_calls": [],
            "conversation_history": [],
            "session_id": "test-session",
            "metadata": {},
            "final_response": "",
            "status": "",
            "next_steps": [],
        }

        result = app.invoke(initial_state)
        dashboard = result.get("metadata", {}).get("execution_dashboard", {})

        if result.get("status") in {"completed", "pending_approval"}:
            print(f"  ✅ workflow status: {result.get('status')}")
        else:
            print(f"  ❌ workflow status: {result.get('status')}")
            return False

        tasks = dashboard.get("tasks", [])
        if len(tasks) >= 5:
            print(f"  ✅ task breakdown generated ({len(tasks)} tasks)")
        else:
            print("  ❌ insufficient task breakdown")
            return False

        if dashboard.get("audit_trail"):
            print("  ✅ audit trail generated")
        else:
            print("  ❌ audit trail missing")
            return False

        if dashboard.get("metrics"):
            print("  ✅ productivity metrics generated")
        else:
            print("  ❌ productivity metrics missing")
            return False

        if dashboard.get("documents") and dashboard.get("emails"):
            print("  ✅ documents and email drafts generated")
        else:
            print("  ❌ artifacts missing (documents/emails)")
            return False

        return True
    except Exception as e:
        print(f"  ❌ Enterprise onboarding error: {e}")
        return False

def main():
    print("=" * 60)
    print("🏢 Intelligent Enterprise Operations Hub - System Test")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Data Files", test_data_files()))
    results.append(("Tools", test_tools()))
    results.append(("Intent Parsing", test_intent_parsing()))
    results.append(("Configuration", test_config()))
    results.append(("Enterprise Store", test_enterprise_store()))
    results.append(("Enterprise Onboarding", test_enterprise_onboarding_workflow()))
    
    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name:20} {status}")
    
    all_passed = all(result[1] for result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! System is ready to run.")
        print("\n🚀 Start the application with:")
        print("   python run.py")
        print("   OR")
        print("   streamlit run app/main.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues before running.")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
