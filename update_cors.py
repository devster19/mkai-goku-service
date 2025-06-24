#!/usr/bin/env python3
"""
Script to add CORS middleware to all agent files
"""

import os
import re


def add_cors_to_file(file_path):
    """Add CORS middleware to a FastAPI agent file"""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if CORS is already added
        if "CORSMiddleware" in content:
            print(f"✓ CORS already exists in {file_path}")
            return

        # Add CORS import
        if "from fastapi import FastAPI" in content:
            content = content.replace(
                "from fastapi import FastAPI",
                "from fastapi import FastAPI\nfrom fastapi.middleware.cors import CORSMiddleware",
            )

        # Add CORS middleware after app creation
        app_pattern = r"(app = FastAPI\([^)]+\))"
        cors_middleware = """app = FastAPI(title="Strategic Agent", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)"""

        content = re.sub(app_pattern, cors_middleware, content)

        # Write back to file
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)

        print(f"✓ Added CORS to {file_path}")

    except Exception as e:
        print(f"✗ Error updating {file_path}: {e}")


def main():
    """Update all agent files"""
    agents_dir = "agents"

    if not os.path.exists(agents_dir):
        print(f"✗ Agents directory not found: {agents_dir}")
        return

    agent_files = [
        "strategic_agent.py",
        "creative_agent.py",
        "financial_agent.py",
        "sales_agent.py",
        "manager_agent.py",
        "analytics_agent.py",
        "swot_agent.py",
        "business_model_agent.py",
    ]

    print("🔧 Adding CORS middleware to all agent files...")

    for agent_file in agent_files:
        file_path = os.path.join(agents_dir, agent_file)
        if os.path.exists(file_path):
            add_cors_to_file(file_path)
        else:
            print(f"⚠️  File not found: {file_path}")

    print("\n✅ CORS middleware added to all agent files!")
    print("🔄 Restart your agents to apply the changes.")


if __name__ == "__main__":
    main()
