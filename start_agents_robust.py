#!/usr/bin/env python3
"""
Robust Multi-Agent Business Analysis System Startup Script
Starts all agent servers with proper error handling and health checks
"""

import asyncio
import subprocess
import sys
import time
import os
import httpx
from pathlib import Path

# Agent configurations
AGENTS = [
    {"name": "Strategic Agent", "script": "agents/strategic_agent.py", "port": 5001},
    {"name": "Creative Agent", "script": "agents/creative_agent.py", "port": 5002},
    {"name": "Financial Agent", "script": "agents/financial_agent.py", "port": 5003},
    {"name": "Sales Agent", "script": "agents/sales_agent.py", "port": 5004},
    {"name": "Manager Agent", "script": "agents/manager_agent.py", "port": 5005},
    {"name": "Analytics Agent", "script": "agents/analytics_agent.py", "port": 5006},
    {"name": "SWOT Agent", "script": "agents/swot_agent.py", "port": 5007},
    {
        "name": "Business Model Canvas Agent",
        "script": "agents/business_model_agent.py",
        "port": 5008,
    },
]


async def check_agent_health(port, timeout=10):
    """Check if an agent is healthy by calling its health endpoint"""
    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(f"http://localhost:{port}/health")
            return response.status_code == 200
    except:
        return False


async def wait_for_agent(port, agent_name, max_wait=30):
    """Wait for an agent to become healthy"""
    print(f"⏳ Waiting for {agent_name} to be ready...")
    start_time = time.time()

    while time.time() - start_time < max_wait:
        if await check_agent_health(port):
            print(f"✓ {agent_name} is healthy")
            return True
        await asyncio.sleep(1)

    print(f"✗ {agent_name} failed to become healthy within {max_wait} seconds")
    return False


async def start_agent(agent_config):
    """Start a single agent server"""
    name = agent_config["name"]
    script = agent_config["script"]
    port = agent_config["port"]

    print(f"🚀 Starting {name} on port {port}...")

    try:
        # Check if script exists
        if not os.path.exists(script):
            print(f"✗ Script not found: {script}")
            return None

        # Start the agent process
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            script,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        # Wait for the agent to become healthy
        if await wait_for_agent(port, name):
            return process
        else:
            # Kill the process if it didn't become healthy
            process.terminate()
            return None

    except Exception as e:
        print(f"✗ Error starting {name}: {e}")
        return None


async def start_all_agents():
    """Start all agent servers with proper sequencing"""
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
                print(f"Stopping {name}...")
                proc.terminate()
                try:
                    await asyncio.wait_for(proc.wait(), timeout=5)
                except asyncio.TimeoutError:
                    proc.kill()
            return False

    print(f"\n✓ All {len(processes)} agents started successfully!")

    # Wait a bit more for all agents to be fully ready
    print("⏳ Waiting for all agents to be fully ready...")
    await asyncio.sleep(5)

    # Start core agent
    print("\n🎯 Starting Core Agent...")
    try:
        core_process = await asyncio.create_subprocess_exec(
            sys.executable,
            "main.py",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        # Wait for core agent to become healthy
        if await wait_for_agent(5099, "Core Agent", max_wait=45):
            processes.append(("Core Agent", core_process))
        else:
            print("✗ Failed to start Core Agent")
            # Stop all processes
            for name, proc in processes:
                print(f"Stopping {name}...")
                proc.terminate()
                try:
                    await asyncio.wait_for(proc.wait(), timeout=5)
                except asyncio.TimeoutError:
                    proc.kill()
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
        # Keep the processes running and monitor them
        while True:
            await asyncio.sleep(5)

            # Check if any process has died
            for name, process in processes:
                if process.returncode is not None:
                    print(
                        f"⚠️  {name} has stopped unexpectedly (return code: {process.returncode})"
                    )

                    # Try to get error output
                    try:
                        stdout, stderr = await process.communicate()
                        if stderr:
                            print(f"Error output from {name}: {stderr.decode()}")
                    except:
                        pass

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
