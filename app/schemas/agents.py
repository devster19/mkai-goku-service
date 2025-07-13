"""
Agent-related Pydantic schemas
"""

from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any, Optional


class AgentType(BaseModel):
    """Agent type definition"""

    type_id: str
    name: str
    description: str
    category: str  # e.g., "analysis", "creative", "financial", "strategic"
    capabilities: List[str]
    is_active: bool = True
    version: str = "1.0.0"


class AgentTypeUpdate(BaseModel):
    """Agent type update model (partial updates)"""

    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    capabilities: Optional[List[str]] = None
    is_active: Optional[bool] = None
    version: Optional[str] = None


class AgentTypeList(BaseModel):
    """List of agent types"""

    agent_types: List[AgentType]
    total_count: int
    category_filter: Optional[str] = None


class AgentRegister(BaseModel):
    """Agent registration model"""

    agent_name: str
    agent_type: (
        str  # e.g., "custom_analytics", "specialized_financial", "market_research"
    )
    endpoint_url: str  # The URL where this agent can be reached
    api_key: Optional[str] = None  # Optional API key for authentication
    description: Optional[str] = None
    capabilities: Optional[List[str]] = None  # List of capabilities this agent provides
    callback_url: Optional[str] = None  # URL for receiving results from this agent
    status: Optional[str] = "active"  # active, inactive, maintenance
    version: Optional[str] = "1.0.0"
    contact_info: Optional[Dict[str, str]] = None  # email, phone, etc.
    configuration: Optional[Dict[str, Any]] = None  # Any additional configuration
    mcp_support: Optional[bool] = False  # Whether this agent supports MCP protocol


class AgentUpdate(BaseModel):
    """Agent update model"""

    agent_name: Optional[str] = None
    description: Optional[str] = None
    capabilities: Optional[List[str]] = None
    endpoint_url: Optional[str] = None
    callback_url: Optional[str] = None
    api_key: Optional[str] = None
    status: Optional[str] = None
    version: Optional[str] = None
    contact_info: Optional[Dict[str, str]] = None
    configuration: Optional[Dict[str, Any]] = None
    mcp_support: Optional[bool] = None


class AgentResponse(BaseModel):
    """Agent response model"""

    agent_id: str
    agent_name: str
    agent_type: str
    description: str
    capabilities: List[str]
    endpoint_url: str
    callback_url: Optional[str] = None
    api_key: Optional[str] = None
    status: str
    version: str
    contact_info: Optional[Dict[str, str]] = None
    configuration: Optional[Dict[str, Any]] = None
    mcp_support: bool
    created_at: str
    updated_at: str


class SimpleAgentRegistration(BaseModel):
    """Simple agent registration model (ChatGPT example style)"""

    name: str
    callback_url: HttpUrl


class AgentListResponse(BaseModel):
    """Response model for agent listing"""

    agents: List[AgentResponse]
    total_count: int
    status_filter: Optional[str] = None
    agent_type_filter: Optional[str] = None


class AgentSearchResponse(BaseModel):
    """Response model for agent search"""

    agents: List[AgentResponse]
    total_count: int
    search_query: str
