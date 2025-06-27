"""
Database operations and connection management
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging

from app.core.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseManager:
    """Database connection and operations manager"""

    def __init__(self):
        self.client: Optional[MongoClient] = None
        self.db = None
        self._collections = {}

    def connect(self) -> bool:
        """Connect to MongoDB"""
        try:
            # Log the MongoDB URI being used
            logger.warning(f"🚨 Using MongoDB URI: {settings.MONGODB_URI}")

            self.client = MongoClient(
                settings.MONGODB_URI, serverSelectionTimeoutMS=5000
            )
            # Test the connection
            self.client.admin.command("ping")
            logger.info("✅ Successfully connected to MongoDB")

            # Get database and collections
            self.db = self.client.business_analysis
            self._initialize_collections()
            self._create_indexes()

            return True

        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Database connection error: {e}")
            return False

    def _initialize_collections(self):
        """Initialize all database collections"""
        self._collections = {
            "businesses": self.db.businesses,
            "analyses": self.db.analyses,
            "tasks": self.db.tasks,
            "goals": self.db.goals,
            "agents": self.db.agents,
            "agent_types": self.db.agent_types,
            "mcp_tasks": self.db.mcp_tasks,
            "mcp_results": self.db.mcp_results,
            "mcp_task_logs": self.db.mcp_task_logs,
        }

    def _create_indexes(self):
        """Create database indexes for better performance"""
        # Business indexes
        self._collections["businesses"].create_index("business_name")
        self._collections["businesses"].create_index("business_type")
        self._collections["businesses"].create_index("created_at")

        # Analysis indexes
        self._collections["analyses"].create_index("business_id")
        self._collections["analyses"].create_index("created_at")

        # Task indexes
        self._collections["tasks"].create_index("business_id")
        self._collections["tasks"].create_index("status")
        self._collections["tasks"].create_index("next_execution")

        # Goal indexes
        self._collections["goals"].create_index("business_id")
        self._collections["goals"].create_index("status")

        # Agent indexes
        self._collections["agents"].create_index("agent_name")
        self._collections["agents"].create_index("agent_type")
        self._collections["agents"].create_index("status")
        self._collections["agents"].create_index("created_at")

        # Agent type indexes
        self._collections["agent_types"].create_index("type_id")
        self._collections["agent_types"].create_index("category")
        self._collections["agent_types"].create_index("is_active")

        # MCP task indexes
        self._collections["mcp_tasks"].create_index("description")
        self._collections["mcp_tasks"].create_index("task_type")
        self._collections["mcp_tasks"].create_index("priority")
        self._collections["mcp_tasks"].create_index("status")
        self._collections["mcp_tasks"].create_index("agent_id")
        self._collections["mcp_tasks"].create_index("created_at")

        # MCP result indexes
        self._collections["mcp_results"].create_index("task_id")
        self._collections["mcp_results"].create_index("agent_id")
        self._collections["mcp_results"].create_index("status")
        self._collections["mcp_results"].create_index("created_at")

        # MCP task logs indexes
        self._collections["mcp_task_logs"].create_index("task_id")
        self._collections["mcp_task_logs"].create_index("agent_id")
        self._collections["mcp_task_logs"].create_index("status")
        self._collections["mcp_task_logs"].create_index("attempted_at")

    def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("🔌 Disconnected from MongoDB")

    def get_collection(self, name: str):
        """Get a collection by name"""
        if not self.client:
            if not self.connect():
                raise ConnectionError("Failed to connect to database")
        return self._collections.get(name)

    def _convert_object_id(self, doc: Dict[str, Any]) -> Dict[str, Any]:
        """Convert ObjectId to string and datetime to ISO format"""
        if doc and "_id" in doc:
            # Map _id to business_id for business documents
            if "business_name" in doc:
                doc["business_id"] = str(doc["_id"])
            doc["_id"] = str(doc["_id"])

        # Convert datetime objects to ISO strings
        for key, value in doc.items():
            if isinstance(value, datetime):
                doc[key] = value.isoformat()

        return doc

    def _convert_documents(
        self, documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Convert multiple documents"""
        return [self._convert_object_id(doc) for doc in documents]

    def _get_current_time(self) -> str:
        """Get current time in ISO format"""
        return datetime.utcnow().isoformat()


# Global database instance
db = DatabaseManager()
