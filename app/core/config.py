"""
Application configuration and settings
"""
import os
from typing import Optional, List
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings"""
    
    def __init__(self):
        # API Configuration
        self.API_V1_STR: str = "/api/v1"
        self.PROJECT_NAME: str = "Multi-Agent Business Analysis System"
        self.VERSION: str = "1.0.1"
        self.API_URL: str = os.getenv("API_URL", "http://localhost:8000/api/v1")
        
        # Database Configuration
        self.MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb://localhost:27017/business_analysis")
        
        # CORS Configuration
        self.BACKEND_CORS_ORIGINS: List[str] = ["*"]
        
        # External Agents Configuration
        self.DEFAULT_AGENT_TIMEOUT: int = int(os.getenv("DEFAULT_AGENT_TIMEOUT", "30"))
        self.MAX_AGENT_RETRIES: int = int(os.getenv("MAX_AGENT_RETRIES", "3"))
        
        # Task Automation Configuration
        self.AUTOMATION_ENABLED: bool = os.getenv("AUTOMATION_ENABLED", "true").lower() == "true"
        self.SCHEDULER_INTERVAL: int = int(os.getenv("SCHEDULER_INTERVAL", "60"))


# Global settings instance
settings = Settings() 