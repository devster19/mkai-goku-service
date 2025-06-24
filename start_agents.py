#!/usr/bin/env python3
"""
Multi-Agent Business Analysis System Startup Script
Starts all agent servers in parallel
"""

import asyncio
import subprocess
import sys
import time
import os
from pathlib import Path

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


def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import uvicorn
        import openai
        import httpx

        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False


def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists(".env"):
        print("⚠️  .env file not found. Creating from example...")
        if os.path.exists("config.env.example"):
            import shutil

            shutil.copy("config.env.example", ".env")
            print("✓ Created .env file from example")
            print("⚠️  Please update .env file with your OpenAI API key")
        else:
            print("✗ config.env.example not found")
            return False
    return True


async def start_agent(agent_config):
    """Start a single agent server"""
    name = agent_config["name"]
    script = agent_config["script"]
    port = agent_config["port"]

    print(f"Starting {name} on port {port}...")

    try:
        # Start the agent process
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            script,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        # Wait a bit for the server to start
        await asyncio.sleep(2)

        if process.returncode is None:
            print(f"✓ {name} started successfully on port {port}")
            return process
        else:
            print(f"✗ Failed to start {name}")
            return None

    except Exception as e:
        print(f"✗ Error starting {name}: {e}")
        return None


async def start_all_agents():
    """Start all agent servers"""
    print("🚀 Starting Multi-Agent Business Analysis System...")
    print("=" * 50)

    # Check dependencies and environment
    if not check_dependencies():
        return False

    if not check_env_file():
        return False

    print("\n📋 Agent Configuration:")
    for agent in AGENTS:
        print(f"  • {agent['name']}: http://localhost:{agent['port']}")

    print("\n🔄 Starting agents...")

    # Start all agents
    processes = []
    for agent in AGENTS:
        process = await start_agent(agent)
        if process:
            processes.append((agent["name"], process))
        else:
            print(f"✗ Failed to start {agent['name']}, stopping all agents...")
            # Stop all started processes
            for name, proc in processes:
                proc.terminate()
            return False

    print(f"\n✓ All {len(processes)} agents started successfully!")

    # Start core agent
    print("\n🎯 Starting Core Agent...")
    try:
        core_process = await asyncio.create_subprocess_exec(
            sys.executable,
            "main.py",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        await asyncio.sleep(3)

        if core_process.returncode is None:
            print("✓ Core Agent started successfully on http://localhost:5099")
            processes.append(("Core Agent", core_process))
        else:
            print("✗ Failed to start Core Agent")
            return False

    except Exception as e:
        print(f"✗ Error starting Core Agent: {e}")
        return False

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
            await asyncio.sleep(1)

            # Check if any process has died
            for name, process in processes:
                if process.returncode is not None:
                    print(f"⚠️  {name} has stopped unexpectedly")
                    return False

    except KeyboardInterrupt:
        print("\n\n🛑 Stopping all agents...")

        # Stop all processes
        for name, process in processes:
            print(f"Stopping {name}...")
            process.terminate()
            try:
                await asyncio.wait_for(process.wait(), timeout=5)
            except asyncio.TimeoutError:
                process.kill()

        print("✓ All agents stopped")
        return True


def main():
    """Main function"""
    try:
        asyncio.run(start_all_agents())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
