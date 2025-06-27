"""
Task-related Pydantic schemas
"""
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import secrets
import hashlib
import time


class MCPContext(BaseModel):
    """MCP context model with memory and retriever"""
    memory: Optional[str] = None
    retriever: Optional[List[str]] = None


class MediaItem(BaseModel):
    """Media item model for images, videos, etc."""
    url: str
    caption: Optional[str] = None
    alt_text: Optional[str] = None
    type: Optional[str] = "image"  # image, video, audio, etc.


class LinkItem(BaseModel):
    """Link item model"""
    title: str
    url: str
    description: Optional[str] = None


class FileItem(BaseModel):
    """File item model"""
    filename: str
    url: str
    size: Optional[int] = None
    mime_type: Optional[str] = None


class TaskOutput(BaseModel):
    """Enhanced task output with rich content"""
    text: Optional[str] = None
    images: Optional[List[MediaItem]] = None
    links: Optional[List[LinkItem]] = None
    files: Optional[List[FileItem]] = None
    data: Optional[Dict[str, Any]] = None  # For structured data
    html: Optional[str] = None  # For HTML content
    markdown: Optional[str] = None  # For markdown content


class ContextUpdate(BaseModel):
    """Context update model"""
    memory: Optional[str] = None
    tags: Optional[List[str]] = None
    metadata: Optional[Dict[str, Any]] = None


class MCPTaskRequest(BaseModel):
    """MCP standard task request model"""
    description: str
    type: str  # e.g., "content_generation", "analysis", "prediction"
    params: Dict[str, Any]
    context: Optional[MCPContext] = None
    callback_url: Optional[str] = None
    business_id: Optional[str] = Field(None, description="Business ID this task belongs to")


class MCPTaskCreate(BaseModel):
    """MCP task creation model (internal use)"""
    description: str
    type: str
    params: Dict[str, Any]
    context: Optional[MCPContext] = None
    callback_url: Optional[str] = None
    business_id: Optional[str] = None  # Associate task with a specific business


class MCPTaskUpdate(BaseModel):
    """MCP task update model"""
    status: Optional[str] = None  # pending, in_progress, completed, failed
    params: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    context: Optional[MCPContext] = None
    callback_url: Optional[str] = None
    business_id: Optional[str] = None  # Update business association


class MCPTaskResult(BaseModel):
    """Enhanced MCP task result model with rich content"""
    task_id: Optional[str] = None
    agent_id: Optional[str] = None
    status: Optional[str] = "completed"
    output: Optional[TaskOutput] = None
    context_update: Optional[ContextUpdate] = None
    execution_time: Optional[float] = None
    error_message: Optional[str] = None
    timestamp: Optional[str] = None


class MCPCallbackRequest(BaseModel):
    """MCP callback request model"""
    callback_url: Optional[str] = None
    result_data: MCPTaskResult


class MCPTaskResponse(BaseModel):
    """Enhanced MCP task response model (internal representation)"""
    task_id: str
    agent_id: str
    business_id: Optional[str] = None  # Business this task belongs to
    type: str
    params: Dict[str, Any]
    status: str  # pending, in_progress, completed, failed
    result: Optional[Dict[str, Any]] = None  # Legacy result field
    output: Optional[TaskOutput] = None  # New enhanced output field
    context: Optional[MCPContext] = None
    context_update: Optional[ContextUpdate] = None  # New context update field
    callback_url: Optional[str] = None  # Now contains the secure callback URL
    created_at: str
    updated_at: str


class MCPResult(BaseModel):
    """MCP result model"""
    task_id: str
    agent_id: str
    business_id: Optional[str] = None
    status: str  # success, failed, partial
    result: Dict[str, Any]
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
    timestamp: str


class TaskResult(BaseModel):
    """Enhanced task result model for storing detailed results"""
    result_id: str
    task_id: str
    agent_id: str
    business_id: Optional[str] = None
    status: str  # success, failed, partial
    result: Optional[Dict[str, Any]] = None  # Legacy result field
    output: Optional[TaskOutput] = None  # New enhanced output field
    context_update: Optional[ContextUpdate] = None  # New context update field
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: str


class SecureCallbackInfo(BaseModel):
    """Secure callback information"""
    original_url: str
    secure_url: str
    token: str
    expires_at: int


# Legacy models for backward compatibility
class TaskRequest(BaseModel):
    """Simple task request model (ChatGPT example style) - DEPRECATED"""
    description: str
    type: str  # e.g., "content_generation"
    params: Dict[str, Any]
    context: Dict[str, Any]
    callback_url: str


class TaskCreate(BaseModel):
    """Task creation model for automation"""
    business_name: str
    agent_type: str
    task_type: str
    frequency: str
    parameters: Optional[Dict[str, Any]] = {}
    status: Optional[str] = "pending"


class TaskUpdate(BaseModel):
    """Task update model for automation"""
    status: Optional[str] = None
    results: Optional[Dict[str, Any]] = None
    last_executed: Optional[str] = None
    next_execution: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None


class TaskListResponse(BaseModel):
    """Response model for task listing"""
    tasks: List[Dict[str, Any]]
    total_count: int
    status_filter: Optional[str] = None
    agent_id_filter: Optional[str] = None


class TaskResultResponse(BaseModel):
    """Response model for task result"""
    status: str
    task_id: str
    result_id: Optional[str] = None 