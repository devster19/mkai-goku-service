#!/usr/bin/env python3
"""
Diagnostic script for Multi-Agent Business Analysis System
Checks system requirements and identifies potential issues
"""

import os
import sys
import importlib
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")

    if version.major == 3 and version.minor >= 8:
        print("   ✓ Python version is compatible")
        return True
    else:
        print("   ✗ Python 3.8+ is required")
        return False


def check_virtual_environment():
    """Check if virtual environment is activated"""
    print("\n🔧 Checking virtual environment...")

    if hasattr(sys, "real_prefix") or (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print("   ✓ Virtual environment is activated")
        print(f"   Virtual env: {sys.prefix}")
        return True
    else:
        print("   ✗ Virtual environment not detected")
        print("   Please activate the virtual environment:")
        print("   source venv/bin/activate  # On Unix/macOS")
        print("   venv\\Scripts\\activate     # On Windows")
        return False


def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\n📄 Checking .env file...")

    if not os.path.exists(".env"):
        print("   ✗ .env file not found")
        print("   Please run: python setup.py")
        return False

    print("   ✓ .env file exists")

    # Check for required variables
    required_vars = ["OPENAI_API_KEY"]
    missing_vars = []

    with open(".env", "r") as f:
        content = f.read()
        for var in required_vars:
            if f"{var}=" not in content:
                missing_vars.append(var)

    if missing_vars:
        print(f"   ✗ Missing required variables: {', '.join(missing_vars)}")
        return False
    else:
        print("   ✓ All required variables found")
        return True


def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")

    required_packages = [
        "fastapi",
        "uvicorn",
        "httpx",
        "openai",
        "python-dotenv",
        "pydantic",
    ]

    missing_packages = []

    for package in required_packages:
        try:
            importlib.import_module(package.replace("-", "_"))
            print(f"   ✓ {package}")
        except ImportError:
            print(f"   ✗ {package} (missing)")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n   Missing packages: {', '.join(missing_packages)}")
        print("   Please install dependencies:")
        print("   pip install -r requirements.txt")
        return False

    return True


def check_agent_files():
    """Check if all agent files exist"""
    print("\n🤖 Checking agent files...")

    agent_files = [
        "agents/strategic_agent.py",
        "agents/creative_agent.py",
        "agents/financial_agent.py",
        "agents/sales_agent.py",
        "agents/manager_agent.py",
        "agents/analytics_agent.py",
        "agents/swot_agent.py",
        "agents/business_model_agent.py",
    ]

    missing_files = []

    for file_path in agent_files:
        if os.path.exists(file_path):
            print(f"   ✓ {file_path}")
        else:
            print(f"   ✗ {file_path} (missing)")
            missing_files.append(file_path)

    if missing_files:
        print(f"\n   Missing files: {len(missing_files)}")
        return False

    return True


def check_ports():
    """Check if required ports are available"""
    print("\n🔌 Checking port availability...")

    ports = [5000, 5001, 5002, 5003, 5004, 5005, 5006, 5007, 5008]
    occupied_ports = []

    for port in ports:
        try:
            import socket

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                result = s.connect_ex(("localhost", port))
                if result == 0:
                    print(f"   ⚠️  Port {port} is occupied")
                    occupied_ports.append(port)
                else:
                    print(f"   ✓ Port {port} is available")
        except Exception as e:
            print(f"   ? Port {port} check failed: {e}")

    if occupied_ports:
        print(f"\n   Occupied ports: {', '.join(map(str, occupied_ports))}")
        print("   Please stop any services using these ports")
        return False

    return True


def check_openai_api():
    """Test OpenAI API connection"""
    print("\n🔑 Testing OpenAI API...")

    try:
        from dotenv import load_dotenv

        load_dotenv()

        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("   ✗ OPENAI_API_KEY not found in environment")
            return False

        if api_key == "your-openai-api-key-here":
            print("   ✗ OPENAI_API_KEY not configured (still using placeholder)")
            return False

        print("   ✓ OPENAI_API_KEY found")

        # Test API connection
        try:
            import openai

            client = openai.OpenAI(api_key=api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5,
            )
            print("   ✓ OpenAI API connection successful")
            return True
        except Exception as e:
            print(f"   ✗ OpenAI API connection failed: {e}")
            return False

    except Exception as e:
        print(f"   ✗ Error testing OpenAI API: {e}")
        return False


def main():
    """Run all diagnostic checks"""
    print("🔍 Multi-Agent Business Analysis System Diagnostic")
    print("=" * 50)

    checks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_virtual_environment),
        ("Environment File", check_env_file),
        ("Dependencies", check_dependencies),
        ("Agent Files", check_agent_files),
        ("Port Availability", check_ports),
        ("OpenAI API", check_openai_api),
    ]

    results = []

    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"   ✗ Error during {name} check: {e}")
            results.append((name, False))

    print("\n" + "=" * 50)
    print("📊 Diagnostic Results:")

    passed = 0
    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"   {status} {name}")
        if result:
            passed += 1

    print(f"\n🎯 Summary: {passed}/{len(results)} checks passed")

    if passed == len(results):
        print("🎉 All checks passed! The system should work correctly.")
        print("\n💡 Next steps:")
        print("   1. Run: python start_agents_robust.py")
        print("   2. Test: python test_system.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\n💡 Common solutions:")
        print("   1. Activate virtual environment: source venv/bin/activate")
        print("   2. Install dependencies: pip install -r requirements.txt")
        print("   3. Set up environment: python setup.py")
        print("   4. Configure OpenAI API key in .env file")
        print("   5. Stop services using ports 5000-5008")


if __name__ == "__main__":
    main()
