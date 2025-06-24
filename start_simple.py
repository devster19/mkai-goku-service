#!/usr/bin/env python3
"""
Simple startup script for Multi-Agent Business Analysis System
Starts each agent individually with better error handling
"""

import subprocess
import sys
import time
import os
import signal
import threading

# Agent configurations
AGENTS = [
    ("Strategic Agent", "agents/strategic_agent.py", 5001),
    ("Creative Agent", "agents/creative_agent.py", 5002),
    ("Financial Agent", "agents/financial_agent.py", 5003),
    ("Sales Agent", "agents/sales_agent.py", 5004),
    ("Manager Agent", "agents/manager_agent.py", 5005),
    ("Analytics Agent", "agents/analytics_agent.py", 5006),
    ("SWOT Agent", "agents/swot_agent.py", 5007),
    ("Business Model Canvas Agent", "agents/business_model_agent.py", 5008),
]

processes = []


def start_agent(name, script, port):
    """Start a single agent"""
    print(f"🚀 Starting {name} on port {port}...")

    try:
        # Check if script exists
        if not os.path.exists(script):
            print(f"✗ Script not found: {script}")
            return None

        # Start the agent process
        process = subprocess.Popen(
            [sys.executable, script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        # Wait a bit for the process to start
        time.sleep(2)

        # Check if process is still running
        if process.poll() is None:
            print(f"✓ {name} started successfully (PID: {process.pid})")
            return process
        else:
            # Process died, get error output
            stdout, stderr = process.communicate()
            print(f"✗ {name} failed to start")
            if stderr:
                print(f"  Error: {stderr}")
            return None

    except Exception as e:
        print(f"✗ Error starting {name}: {e}")
        return None


def check_agent_health(port, name):
    """Check if an agent is healthy"""
    import requests

    try:
        response = requests.get(f"http://localhost:{port}/health", timeout=5)
        if response.status_code == 200:
            print(f"✓ {name} is healthy")
            return True
        else:
            print(f"✗ {name} unhealthy (Status: {response.status_code})")
            return False
    except Exception as e:
        print(f"✗ {name} health check failed: {e}")
        return False


def main():
    """Main startup function"""
    print("🚀 Starting Multi-Agent Business Analysis System...")
    print("=" * 50)

    # Check if virtual environment is activated
    if not hasattr(sys, "real_prefix") and not (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix
    ):
        print("⚠️  Virtual environment not detected. Please activate it first:")
        print("   source venv/bin/activate  # On Unix/macOS")
        print("   venv\\Scripts\\activate     # On Windows")
        return False

    # Check if .env file exists
    if not os.path.exists(".env"):
        print("❌ .env file not found. Please run setup first:")
        print("   python setup.py")
        return False

    print("\n📋 Starting agents...")

    # Start all agents
    for name, script, port in AGENTS:
        process = start_agent(name, script, port)
        if process:
            processes.append((name, process, port))
        else:
            print(f"✗ Failed to start {name}, stopping all agents...")
            # Stop all started processes
            for pname, pprocess, pport in processes:
                print(f"Stopping {pname}...")
                pprocess.terminate()
                try:
                    pprocess.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    pprocess.kill()
            return False

    print(f"\n✓ All {len(processes)} agents started successfully!")

    # Wait for agents to be ready
    print("\n⏳ Waiting for agents to be ready...")
    time.sleep(10)

    # Check agent health
    print("\n🔍 Checking agent health...")
    healthy_agents = 0
    for name, process, port in processes:
        if check_agent_health(port, name):
            healthy_agents += 1

    if healthy_agents < len(processes):
        print(f"\n⚠️  Only {healthy_agents}/{len(processes)} agents are healthy")
    else:
        print(f"\n✓ All {healthy_agents} agents are healthy!")

    # Start Core Agent
    print("\n🎯 Starting Core Agent...")
    try:
        core_process = subprocess.Popen(
            [sys.executable, "main.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        time.sleep(5)

        if core_process.poll() is None:
            print("✓ Core Agent started successfully")
            processes.append(("Core Agent", core_process, 5099))
        else:
            stdout, stderr = core_process.communicate()
            print("✗ Core Agent failed to start")
            if stderr:
                print(f"Error: {stderr}")
            return False

    except Exception as e:
        print(f"✗ Error starting Core Agent: {e}")
        return False

    # Check Core Agent health
    time.sleep(3)
    if check_agent_health(5099, "Core Agent"):
        print("\n🎉 Multi-Agent System is ready!")
        print("=" * 50)
        print("📊 Core Agent API: http://localhost:5099")
        print("📚 API Documentation: http://localhost:5099/docs")
        print("🔍 Health Check: http://localhost:5099/health")
        print("\n💡 Example request:")
        print(
            """
curl -X POST "http://localhost:5099/process-business" \\
     -H "Content-Type: application/json" \\
     -d '{
       "business_name": "ร้านกาแฟสดใจดี",
       "location": "กรุงเทพมหานคร",
       "competitors": ["ร้านกาแฟ Amazon", "ร้านกาแฟ All Cafe"],
       "growth_goals": ["เพิ่มยอดขาย 50% ภายใน 1 ปี", "ขยายสาขาใหม่"]
     }'
        """
        )

        print("\n⏹️  Press Ctrl+C to stop all agents...")

        try:
            # Keep the processes running
            while True:
                time.sleep(5)

                # Check if any process has died
                for name, process, port in processes:
                    if process.poll() is not None:
                        print(f"⚠️  {name} has stopped unexpectedly")
                        return False

        except KeyboardInterrupt:
            print("\n\n🛑 Stopping all agents...")

            # Stop all processes
            for name, process, port in processes:
                print(f"Stopping {name}...")
                process.terminate()
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    process.kill()

            print("✓ All agents stopped")
            return True
    else:
        print("✗ Core Agent is not healthy")
        return False


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
