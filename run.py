import subprocess
import sys
import os

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("⚠️  Warning: .env file not found!")
        print("📝 Creating .env from .env.example...")
        if os.path.exists('.env.example'):
            with open('.env.example', 'r') as example:
                with open('.env', 'w') as env:
                    env.write(example.read())
            print("✅ .env file created. Please add your OPENAI_API_KEY")
            print("📝 Edit .env file and add: OPENAI_API_KEY=your_key_here")
            return False
        else:
            print("❌ .env.example not found!")
            return False
    return True

def check_dependencies():
    """Check if dependencies are installed"""
    try:
        import streamlit
        import langgraph
        import langchain
        return True
    except ImportError:
        print("⚠️  Dependencies not installed!")
        print("📦 Installing dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        return True

def main():
    print("🏢 Intelligent Enterprise Operations Hub")
    print("=" * 50)
    
    if not check_env_file():
        sys.exit(1)
    
    if not check_dependencies():
        sys.exit(1)
    
    # Check if port is specified as command line argument
    port = "8501"
    if len(sys.argv) > 1:
        port = sys.argv[1]
    
    print(f"\n🚀 Starting Streamlit application...")
    print(f"📱 The app will open in your browser at http://localhost:{port}")
    print("⏹️  Press Ctrl+C to stop the server\n")
    
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app/main.py", "--server.port", port])

if __name__ == "__main__":
    main()
