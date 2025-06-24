#!/usr/bin/env python3
"""
Setup script for Multi-Agent Business Analysis System
Helps with initial configuration and dependency installation
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python version: {sys.version}")
    return True


def create_virtual_environment():
    """Create virtual environment if it doesn't exist"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("📦 Creating virtual environment...")
        try:
            subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
            print("✓ Virtual environment created")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to create virtual environment")
            return False
    else:
        print("✓ Virtual environment already exists")
        return True


def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")

    # Determine the pip command based on OS
    if os.name == "nt":  # Windows
        pip_cmd = "venv\\Scripts\\pip"
    else:  # Unix/Linux/macOS
        pip_cmd = "venv/bin/pip"

    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("✓ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False


def setup_environment_file():
    """Set up environment configuration file"""
    env_file = Path(".env")
    example_file = Path("config.env.example")

    if not env_file.exists():
        if example_file.exists():
            print("📝 Creating .env file from example...")
            shutil.copy(example_file, env_file)
            print("✓ .env file created")
            print("⚠️  IMPORTANT: Please edit .env file and add your OpenAI API key")
            return True
        else:
            print("❌ config.env.example not found")
            return False
    else:
        print("✓ .env file already exists")
        return True


def check_openai_api_key():
    """Check if OpenAI API key is configured"""
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file, "r") as f:
            content = f.read()
            if "your_openai_api_key_here" in content:
                print("⚠️  Please update .env file with your actual OpenAI API key")
                return False
            elif "OPENAI_API_KEY=" in content:
                print("✓ OpenAI API key appears to be configured")
                return True
            else:
                print("⚠️  OpenAI API key not found in .env file")
                return False
    else:
        print("❌ .env file not found")
        return False


def create_directories():
    """Create necessary directories"""
    directories = ["agents", "logs", "data"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    print("✓ Directories created")


def main():
    """Main setup function"""
    print("🚀 Multi-Agent Business Analysis System Setup")
    print("=" * 50)

    # Check Python version
    if not check_python_version():
        sys.exit(1)

    # Create virtual environment
    if not create_virtual_environment():
        sys.exit(1)

    # Install dependencies
    if not install_dependencies():
        sys.exit(1)

    # Setup environment file
    if not setup_environment_file():
        sys.exit(1)

    # Create directories
    create_directories()

    # Check OpenAI API key
    api_key_configured = check_openai_api_key()

    print("\n🎉 Setup completed!")
    print("=" * 50)

    if not api_key_configured:
        print("\n📝 Next steps:")
        print("1. Edit .env file and add your OpenAI API key")
        print("2. Run: python start_agents.py")
        print("3. Test the system: python test_system.py")
    else:
        print("\n🚀 Ready to start!")
        print("Run: python start_agents.py")
        print("Test: python test_system.py")

    print("\n📚 For more information, see README.md")


if __name__ == "__main__":
    main()
