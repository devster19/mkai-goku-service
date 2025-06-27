"""
Agent service for handling agent operations
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import logging

from app.core.database import db
from app.schemas.agents import AgentRegister, AgentUpdate, AgentResponse, AgentType, AgentTypeList
from app.core.config import settings

logger = logging.getLogger(__name__)


class AgentService:
    """Service for agent operations"""

    def register_agent(self, agent_data: AgentRegister) -> Optional[AgentResponse]:
        """Register a new agent"""
        try:
            # Validate that the agent type exists
            agent_type = self.get_agent_type(agent_data.agent_type)
            if agent_type is None:
                logger.error(f"❌ Agent type '{agent_data.agent_type}' not found")
                return None
            
            if not agent_type.is_active:
                logger.error(f"❌ Agent type '{agent_data.agent_type}' is not active")
                return None

            collection = db.get_collection("agents")
            if collection is None:
                return None

            # Prepare agent document with only non-None values
            agent_doc = {
                "agent_name": agent_data.agent_name,
                "agent_type": agent_data.agent_type,
                "endpoint_url": agent_data.endpoint_url,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }

            # Add optional fields only if they are not None
            if agent_data.description is not None:
                agent_doc["description"] = agent_data.description
            else:
                agent_doc["description"] = f"Agent of type {agent_data.agent_type}"

            if agent_data.capabilities is not None:
                agent_doc["capabilities"] = agent_data.capabilities
            else:
                agent_doc["capabilities"] = []

            if agent_data.callback_url is not None:
                agent_doc["callback_url"] = agent_data.callback_url

            if agent_data.api_key is not None:
                agent_doc["api_key"] = agent_data.api_key

            if agent_data.status is not None:
                agent_doc["status"] = agent_data.status
            else:
                agent_doc["status"] = "active"

            if agent_data.version is not None:
                agent_doc["version"] = agent_data.version
            else:
                agent_doc["version"] = "1.0.0"

            if agent_data.contact_info is not None:
                agent_doc["contact_info"] = agent_data.contact_info

            if agent_data.configuration is not None:
                agent_doc["configuration"] = agent_data.configuration

            if agent_data.mcp_support is not None:
                agent_doc["mcp_support"] = agent_data.mcp_support
            else:
                agent_doc["mcp_support"] = False

            # Insert agent document
            result = collection.insert_one(agent_doc)
            agent_id = str(result.inserted_id)

            logger.info(f"✅ Saved agent '{agent_data.agent_name}' with ID: {agent_id}")
            
            # Return the created agent
            return self.get_agent(agent_id)

        except Exception as e:
            logger.error(f"❌ Error saving agent: {e}")
            return None

    def get_agent(self, agent_id: str) -> Optional[AgentResponse]:
        """Get agent by ID"""
        try:
            collection = db.get_collection("agents")
            if collection is None:
                return None

            from bson import ObjectId
            agent = collection.find_one({"_id": ObjectId(agent_id)})
            
            if not agent:
                return None

            agent = db._convert_object_id(agent)
            return AgentResponse(
                agent_id=agent["_id"],
                agent_name=agent["agent_name"],
                agent_type=agent["agent_type"],
                description=agent["description"],
                capabilities=agent["capabilities"],
                endpoint_url=agent["endpoint_url"],
                callback_url=agent.get("callback_url"),
                status=agent["status"],
                version=agent["version"],
                contact_info=agent.get("contact_info"),
                configuration=agent.get("configuration"),
                mcp_support=agent.get("mcp_support", False),
                created_at=agent["created_at"],
                updated_at=agent["updated_at"]
            )

        except Exception as e:
            logger.error(f"❌ Error retrieving agent: {e}")
            return None

    def get_all_agents(self, status: Optional[str] = None, agent_type: Optional[str] = None) -> List[AgentResponse]:
        """Get all agents with optional filtering"""
        try:
            collection = db.get_collection("agents")
            if collection is None:
                return []

            query = {}
            if status:
                query["status"] = status
            if agent_type:
                query["agent_type"] = agent_type

            agents = list(collection.find(query))
            agents = db._convert_documents(agents)

            return [
                AgentResponse(
                    agent_id=agent["_id"],
                    agent_name=agent["agent_name"],
                    agent_type=agent["agent_type"],
                    description=agent["description"],
                    capabilities=agent["capabilities"],
                    endpoint_url=agent["endpoint_url"],
                    callback_url=agent.get("callback_url"),
                    status=agent["status"],
                    version=agent["version"],
                    contact_info=agent.get("contact_info"),
                    configuration=agent.get("configuration"),
                    mcp_support=agent.get("mcp_support", False),
                    created_at=agent["created_at"],
                    updated_at=agent["updated_at"]
                )
                for agent in agents
            ]

        except Exception as e:
            logger.error(f"❌ Error retrieving agents: {e}")
            return []

    def update_agent(self, agent_id: str, update_data: AgentUpdate) -> Optional[AgentResponse]:
        """Update an agent"""
        try:
            collection = db.get_collection("agents")
            if collection is None:
                return None

            from bson import ObjectId

            # Convert Pydantic model to dict, excluding None values
            update_dict = {
                k: v for k, v in update_data.model_dump().items() if v is not None
            }

            if not update_dict:
                return None

            # Add updated_at timestamp
            update_dict["updated_at"] = datetime.utcnow()

            result = collection.update_one(
                {"_id": ObjectId(agent_id)}, {"$set": update_dict}
            )

            success = result.modified_count > 0
            if success:
                logger.info(f"✅ Updated agent: {agent_id}")
                return self.get_agent(agent_id)
            
            return None

        except Exception as e:
            logger.error(f"❌ Error updating agent: {e}")
            return None

    def delete_agent(self, agent_id: str) -> bool:
        """Delete an agent"""
        try:
            collection = db.get_collection("agents")
            if collection is None:
                return False

            from bson import ObjectId
            result = collection.delete_one({"_id": ObjectId(agent_id)})

            success = result.deleted_count > 0
            if success:
                logger.info(f"✅ Deleted agent: {agent_id}")
            return success

        except Exception as e:
            logger.error(f"❌ Error deleting agent: {e}")
            return False

    def search_agents(self, query: str) -> List[AgentResponse]:
        """Search agents by name, description, or capabilities"""
        try:
            collection = db.get_collection("agents")
            if collection is None:
                return []

            # Create text search query
            search_query = {
                "$or": [
                    {"agent_name": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}},
                    {"capabilities": {"$regex": query, "$options": "i"}},
                ]
            }

            agents = list(collection.find(search_query))
            agents = db._convert_documents(agents)

            return [
                AgentResponse(
                    agent_id=agent["_id"],
                    agent_name=agent["agent_name"],
                    agent_type=agent["agent_type"],
                    description=agent["description"],
                    capabilities=agent["capabilities"],
                    endpoint_url=agent["endpoint_url"],
                    callback_url=agent.get("callback_url"),
                    status=agent["status"],
                    version=agent["version"],
                    contact_info=agent.get("contact_info"),
                    configuration=agent.get("configuration"),
                    mcp_support=agent.get("mcp_support", False),
                    created_at=agent["created_at"],
                    updated_at=agent["updated_at"]
                )
                for agent in agents
            ]

        except Exception as e:
            logger.error(f"❌ Error searching agents: {e}")
            return []

    def get_agents_by_capability(self, capability: str) -> List[AgentResponse]:
        """Get agents that have a specific capability"""
        try:
            collection = db.get_collection("agents")
            if collection is None:
                return []

            # Find agents with the specified capability
            query = {
                "capabilities": {"$regex": capability, "$options": "i"},
                "status": "active"
            }

            agents = list(collection.find(query))
            agents = db._convert_documents(agents)

            return [
                AgentResponse(
                    agent_id=agent["_id"],
                    agent_name=agent["agent_name"],
                    agent_type=agent["agent_type"],
                    description=agent["description"],
                    capabilities=agent["capabilities"],
                    endpoint_url=agent["endpoint_url"],
                    callback_url=agent.get("callback_url"),
                    status=agent["status"],
                    version=agent["version"],
                    contact_info=agent.get("contact_info"),
                    configuration=agent.get("configuration"),
                    mcp_support=agent.get("mcp_support", False),
                    created_at=agent["created_at"],
                    updated_at=agent["updated_at"]
                )
                for agent in agents
            ]

        except Exception as e:
            logger.error(f"❌ Error getting agents by capability: {e}")
            return []

    # Agent Type Management Methods

    def create_agent_type(self, agent_type_data: AgentType) -> Optional[AgentType]:
        """Create a new agent type"""
        try:
            collection = db.get_collection("agent_types")
            if collection is None:
                return None

            # Check if agent type already exists
            existing = collection.find_one({"type_id": agent_type_data.type_id})
            if existing:
                logger.warning(f"Agent type '{agent_type_data.type_id}' already exists")
                return None

            # Prepare agent type document
            agent_type_doc = {
                "type_id": agent_type_data.type_id,
                "name": agent_type_data.name,
                "description": agent_type_data.description,
                "category": agent_type_data.category,
                "capabilities": agent_type_data.capabilities,
                "is_active": agent_type_data.is_active,
                "version": agent_type_data.version,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }

            # Insert agent type document
            result = collection.insert_one(agent_type_doc)
            type_id = str(result.inserted_id)

            logger.info(f"✅ Created agent type '{agent_type_data.name}' with ID: {type_id}")
            
            return self.get_agent_type(agent_type_data.type_id)

        except Exception as e:
            logger.error(f"❌ Error creating agent type: {e}")
            return None

    def get_agent_type(self, type_id: str) -> Optional[AgentType]:
        """Get agent type by type_id"""
        try:
            collection = db.get_collection("agent_types")
            if collection is None:
                return None

            agent_type = collection.find_one({"type_id": type_id})
            
            if not agent_type:
                return None

            agent_type = db._convert_object_id(agent_type)
            return AgentType(
                type_id=agent_type["type_id"],
                name=agent_type["name"],
                description=agent_type["description"],
                category=agent_type["category"],
                capabilities=agent_type["capabilities"],
                is_active=agent_type["is_active"],
                version=agent_type["version"]
            )

        except Exception as e:
            logger.error(f"❌ Error retrieving agent type: {e}")
            return None

    def get_all_agent_types(self, category: Optional[str] = None, active_only: bool = True) -> List[AgentType]:
        """Get all agent types with optional filtering"""
        try:
            collection = db.get_collection("agent_types")
            if collection is None:
                return []

            query = {}
            if category:
                query["category"] = category
            if active_only:
                query["is_active"] = True

            agent_types = list(collection.find(query))
            agent_types = db._convert_documents(agent_types)

            return [
                AgentType(
                    type_id=agent_type["type_id"],
                    name=agent_type["name"],
                    description=agent_type["description"],
                    category=agent_type["category"],
                    capabilities=agent_type["capabilities"],
                    is_active=agent_type["is_active"],
                    version=agent_type["version"]
                )
                for agent_type in agent_types
            ]

        except Exception as e:
            logger.error(f"❌ Error retrieving agent types: {e}")
            return []

    def update_agent_type(self, type_id: str, update_data) -> Optional[AgentType]:
        """Update an agent type"""
        try:
            collection = db.get_collection("agent_types")
            if collection is None:
                return None

            # Convert Pydantic model to dict, excluding None values
            update_dict = {
                k: v for k, v in update_data.model_dump().items() if v is not None
            }

            if not update_dict:
                return None

            # Add updated_at timestamp
            update_dict["updated_at"] = datetime.utcnow()

            result = collection.update_one(
                {"type_id": type_id}, {"$set": update_dict}
            )

            success = result.modified_count > 0
            if success:
                logger.info(f"✅ Updated agent type: {type_id}")
                return self.get_agent_type(type_id)
            
            return None

        except Exception as e:
            logger.error(f"❌ Error updating agent type: {e}")
            return None

    def delete_agent_type(self, type_id: str) -> bool:
        """Delete an agent type"""
        try:
            collection = db.get_collection("agent_types")
            if collection is None:
                return False

            result = collection.delete_one({"type_id": type_id})

            success = result.deleted_count > 0
            if success:
                logger.info(f"✅ Deleted agent type: {type_id}")
            return success

        except Exception as e:
            logger.error(f"❌ Error deleting agent type: {e}")
            return False

    def initialize_default_agent_types(self) -> bool:
        """Initialize default agent types if they don't exist"""
        try:
            collection = db.get_collection("agent_types")
            if collection is None:
                return False

            # Check if agent types already exist
            existing_count = collection.count_documents({})
            if existing_count > 0:
                logger.info(f"Agent types already exist ({existing_count} found), skipping initialization")
                return True

            # Default agent types
            default_types = [
                AgentType(
                    type_id="analytics_agent",
                    name="Analytics Agent",
                    description="Specialized in data analysis and business intelligence",
                    category="analysis",
                    capabilities=["data_analysis", "business_intelligence", "reporting", "metrics"],
                    is_active=True,
                    version="1.0.0"
                ),
                AgentType(
                    type_id="financial_agent",
                    name="Financial Agent",
                    description="Handles financial analysis, forecasting, and risk assessment",
                    category="financial",
                    capabilities=["financial_analysis", "forecasting", "risk_assessment", "budgeting"],
                    is_active=True,
                    version="1.0.0"
                ),
                AgentType(
                    type_id="creative_agent",
                    name="Creative Agent",
                    description="Generates creative content, ideas, and marketing strategies",
                    category="creative",
                    capabilities=["content_generation", "idea_generation", "marketing_strategy", "branding"],
                    is_active=True,
                    version="1.0.0"
                ),
                AgentType(
                    type_id="strategic_agent",
                    name="Strategic Agent",
                    description="Develops business strategies and long-term planning",
                    category="strategic",
                    capabilities=["strategic_planning", "market_analysis", "competitive_analysis", "business_modeling"],
                    is_active=True,
                    version="1.0.0"
                ),
                AgentType(
                    type_id="sales_agent",
                    name="Sales Agent",
                    description="Manages sales processes and customer relationship management",
                    category="sales",
                    capabilities=["sales_automation", "crm", "lead_generation", "customer_analysis"],
                    is_active=True,
                    version="1.0.0"
                ),
                AgentType(
                    type_id="swot_agent",
                    name="SWOT Analysis Agent",
                    description="Performs SWOT analysis and competitive intelligence",
                    category="analysis",
                    capabilities=["swot_analysis", "competitive_intelligence", "market_research", "risk_assessment"],
                    is_active=True,
                    version="1.0.0"
                ),
                AgentType(
                    type_id="business_model_agent",
                    name="Business Model Agent",
                    description="Analyzes and optimizes business models",
                    category="strategic",
                    capabilities=["business_model_analysis", "revenue_modeling", "cost_structure_analysis", "value_proposition"],
                    is_active=True,
                    version="1.0.0"
                ),
                AgentType(
                    type_id="manager_agent",
                    name="Manager Agent",
                    description="Coordinates and manages other agents and workflows",
                    category="management",
                    capabilities=["workflow_management", "agent_coordination", "project_management", "task_allocation"],
                    is_active=True,
                    version="1.0.0"
                ),
                AgentType(
                    type_id="custom_agent",
                    name="Custom Agent",
                    description="Custom agent with specialized capabilities",
                    category="custom",
                    capabilities=["custom_capabilities"],
                    is_active=True,
                    version="1.0.0"
                )
            ]

            # Insert default agent types
            for agent_type in default_types:
                self.create_agent_type(agent_type)

            logger.info(f"✅ Initialized {len(default_types)} default agent types")
            return True

        except Exception as e:
            logger.error(f"❌ Error initializing default agent types: {e}")
            return False


# Global service instance
agent_service = AgentService() 