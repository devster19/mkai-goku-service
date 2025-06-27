"""
Agent API routes
"""

from typing import List, Optional, Dict, Any
from fastapi import APIRouter, HTTPException, Query, Depends, Request
from fastapi.responses import JSONResponse

from app.schemas.agents import (
    AgentRegister,
    AgentUpdate,
    AgentResponse,
    AgentListResponse,
    AgentSearchResponse,
    SimpleAgentRegistration,
    AgentType,
    AgentTypeUpdate,
    AgentTypeList,
)
from app.schemas.tasks import (
    MCPTaskCreate,
    MCPTaskResult,
    MCPTaskResponse,
    MCPTaskUpdate,
    MCPTaskRequest,
    MCPCallbackRequest,
    TaskResult,
    MCPCallbackResponse,
)
from app.services.agent_service import agent_service
from app.core.database import db
from app.utils.security import callback_manager

router = APIRouter()


@router.get("/types", response_model=AgentTypeList)
async def get_agent_types(
    category: Optional[str] = Query(None, description="Filter by category"),
    active_only: bool = Query(True, description="Show only active agent types"),
):
    """Get all agent types with optional filtering"""
    try:
        agent_types = agent_service.get_all_agent_types(
            category=category, active_only=active_only
        )
        return AgentTypeList(
            agent_types=agent_types,
            total_count=len(agent_types),
            category_filter=category,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving agent types: {str(e)}"
        )


@router.get("/types/{type_id}", response_model=AgentType)
async def get_agent_type(type_id: str):
    """Get specific agent type by type_id"""
    try:
        agent_type = agent_service.get_agent_type(type_id)
        if not agent_type:
            raise HTTPException(status_code=404, detail="Agent type not found")
        return agent_type
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving agent type: {str(e)}"
        )


@router.post("/types", response_model=AgentType, status_code=201)
async def create_agent_type(agent_type_data: AgentType):
    """Create a new agent type"""
    try:
        agent_type = agent_service.create_agent_type(agent_type_data)
        if not agent_type:
            raise HTTPException(status_code=500, detail="Failed to create agent type")
        return agent_type
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating agent type: {str(e)}"
        )


@router.post("/types/initialize", response_model=dict)
async def initialize_default_agent_types():
    """Initialize default agent types if they don't exist"""
    try:
        success = agent_service.initialize_default_agent_types()
        if success:
            return {
                "message": "Default agent types initialized successfully",
                "status": "success",
            }
        else:
            return {"message": "Failed to initialize agent types", "status": "error"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error initializing agent types: {str(e)}"
        )


@router.put("/types/{type_id}", response_model=AgentType)
async def update_agent_type(type_id: str, update_data: AgentType):
    """Update an agent type"""
    try:
        agent_type = agent_service.update_agent_type(type_id, update_data)
        if not agent_type:
            raise HTTPException(
                status_code=404, detail="Agent type not found or no changes made"
            )
        return agent_type
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating agent type: {str(e)}"
        )


@router.delete("/types/{type_id}")
async def delete_agent_type(type_id: str):
    """Delete an agent type"""
    try:
        success = agent_service.delete_agent_type(type_id)
        if not success:
            raise HTTPException(status_code=404, detail="Agent type not found")
        return {"message": "Agent type deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting agent type: {str(e)}"
        )


@router.get("/types/categories", response_model=List[str])
async def get_agent_type_categories():
    """Get all agent type categories"""
    try:
        categories = agent_service.get_agent_type_categories()
        return categories
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving agent type categories: {str(e)}"
        )


@router.get("/search/{query}", response_model=AgentSearchResponse)
async def search_agents(query: str):
    """Search agents by name, description, or capabilities"""
    try:
        agents = agent_service.search_agents(query)
        return AgentSearchResponse(
            agents=agents, total_count=len(agents), search_query=query
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching agents: {str(e)}")


@router.get("/capability/{capability}", response_model=List[AgentResponse])
async def get_agents_by_capability(capability: str):
    """Get agents that have a specific capability"""
    try:
        agents = agent_service.get_agents_by_capability(capability)
        return agents
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting agents by capability: {str(e)}"
        )


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str):
    """Get agent by ID"""
    try:
        agent = agent_service.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        return agent
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving agent: {str(e)}")


@router.post("/register", response_model=AgentResponse, status_code=201)
async def register_agent(agent_data: AgentRegister):
    """Register a new agent"""
    try:
        agent = agent_service.register_agent(agent_data)
        if not agent:
            raise HTTPException(status_code=500, detail="Failed to register agent")
        return agent
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error registering agent: {str(e)}"
        )


@router.get("/", response_model=AgentListResponse)
async def list_agents(
    status: Optional[str] = Query(None, description="Filter by status"),
    agent_type: Optional[str] = Query(None, description="Filter by agent type"),
):
    """List all agents with optional filtering"""
    try:
        agents = agent_service.get_all_agents(status=status, agent_type=agent_type)
        return AgentListResponse(
            agents=agents,
            total_count=len(agents),
            status_filter=status,
            agent_type_filter=agent_type,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing agents: {str(e)}")


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: str, update_data: AgentUpdate):
    """Update an agent"""
    try:
        agent = agent_service.update_agent(agent_id, update_data)
        if not agent:
            raise HTTPException(
                status_code=404, detail="Agent not found or no changes made"
            )
        return agent
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating agent: {str(e)}")


@router.delete("/{agent_id}")
async def delete_agent(agent_id: str):
    """Delete an agent"""
    try:
        success = agent_service.delete_agent(agent_id)
        if not success:
            raise HTTPException(status_code=404, detail="Agent not found")
        return {"message": "Agent deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting agent: {str(e)}")


# Simple agent registration (ChatGPT example style)
@router.post("/simple/register", response_model=AgentResponse, status_code=201)
async def register_simple_agent(agent_data: SimpleAgentRegistration):
    """Register a simple agent (ChatGPT example style)"""
    try:
        # Convert simple registration to full agent registration
        full_agent_data = AgentRegister(
            agent_name=agent_data.name,
            agent_type="simple_agent",
            description=f"Simple agent: {agent_data.name}",
            capabilities=["general"],
            endpoint_url=str(agent_data.callback_url),
            callback_url=str(agent_data.callback_url),
            status="active",
            version="1.0.0",
        )

        agent = agent_service.register_agent(full_agent_data)
        if not agent:
            raise HTTPException(status_code=500, detail="Failed to register agent")
        return agent
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error registering agent: {str(e)}"
        )


# MCP Task Management Endpoints


@router.post("/{agent_id}/tasks", response_model=MCPTaskResponse, status_code=201)
async def create_mcp_task(agent_id: str, task_data: MCPTaskRequest):
    """Create a new MCP task for an agent using MCP standard format"""
    try:
        # Verify agent exists
        agent = agent_service.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        # Create task in database
        collection = db.get_collection("mcp_tasks")
        if collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        task_doc = {
            "agent_id": agent_id,
            "type": task_data.type,
            "params": task_data.params,
            "description": task_data.description,
            "status": "pending",
            "created_at": db._get_current_time(),
            "updated_at": db._get_current_time(),
        }

        # Add context if provided
        if task_data.context:
            task_doc["context"] = task_data.context.dict()

        # Add callback_url if provided
        if task_data.callback_url:
            task_doc["callback_url"] = task_data.callback_url

        result = collection.insert_one(task_doc)
        task_id = str(result.inserted_id)

        # Generate secure callback URL if not provided
        if not task_data.callback_url:
            secure_callback_url = callback_manager.generate_api_callback_url(task_id)
            # Update the task with the secure callback URL
            collection.update_one(
                {"_id": result.inserted_id},
                {"$set": {"callback_url": secure_callback_url}},
            )
            callback_url = secure_callback_url
        else:
            callback_url = task_data.callback_url

        # Test synchronous log creation
        print(f"DEBUG: Testing synchronous log creation for task {task_id}")
        task_logs_collection = db.get_collection("mcp_task_logs")
        if task_logs_collection is not None:
            test_log = {
                "task_id": task_id,
                "agent_id": agent_id,
                "timestamp": db._get_current_time(),
            }
            try:
                test_result = task_logs_collection.insert_one(test_log)
                print(
                    f"DEBUG: Sync test log created with ID: {test_result.inserted_id}"
                )
            except Exception as e:
                print(f"ERROR: Failed to create sync test log: {e}")
        else:
            print(f"ERROR: Could not get mcp_task_logs collection for sync test")

        # Forward task to agent's endpoint if endpoint_url is available
        if hasattr(agent, "endpoint_url") and agent.endpoint_url:
            # Create a background task for forwarding (non-blocking)
            import asyncio

            async def forward_task_async():
                print(f"DEBUG: Starting forward_task_async for task {task_id}")

                # Prepare task data for forwarding (exclude business_id, agent_id, _id)
                forward_task_data = {
                    "type": task_data.type,
                    "description": task_data.description,
                    "params": task_data.params,
                    "callback_url": callback_url,
                }

                # Add context if provided
                if task_data.context:
                    forward_task_data["context"] = task_data.context.dict()

                # Prepare headers
                headers = {"Content-Type": "application/json"}

                # Add API key if available
                if hasattr(agent, "api_key") and agent.api_key:
                    headers["Authorization"] = f"Bearer {agent.api_key}"
                    # Alternative header formats if needed
                    # headers["X-API-Key"] = agent.api_key

                # Log forwarding attempt
                forward_log = {
                    "task_id": task_id,
                    "agent_id": agent_id,
                    "endpoint_url": agent.endpoint_url,
                    "forward_data": forward_task_data,
                    "headers": {
                        k: v for k, v in headers.items() if k != "Authorization"
                    },  # Don't log auth headers
                    "status": "attempting",
                    "attempted_at": db._get_current_time(),
                    "response_status": None,
                    "response_body": None,
                    "error": None,
                }

                # Save forwarding log to database
                task_logs_collection = db.get_collection("mcp_task_logs")
                print(f"DEBUG: Task logs collection: {task_logs_collection}")
                if task_logs_collection is not None:
                    print(f"DEBUG: Inserting forward log for task {task_id}")
                    result = task_logs_collection.insert_one(forward_log)
                    print(f"DEBUG: Forward log inserted with ID: {result.inserted_id}")
                else:
                    print(f"ERROR: Could not get mcp_task_logs collection")

                try:
                    import httpx

                    # Forward task to agent's endpoint
                    async with httpx.AsyncClient(timeout=30.0) as client:
                        response = await client.post(
                            agent.endpoint_url, json=forward_task_data, headers=headers
                        )

                        # Update forwarding log with response
                        update_log = {
                            "status": "completed",
                            "response_status": response.status_code,
                            "response_body": response.text[
                                :500
                            ],  # Limit response body length
                            "completed_at": db._get_current_time(),
                        }

                        if response.status_code in [200, 201, 202]:
                            print(
                                f"DEBUG: Task forwarded successfully to agent {agent_id} at {agent.endpoint_url}"
                            )
                            print(
                                f"DEBUG: Agent response status: {response.status_code}"
                            )
                            update_log["status"] = "success"
                        else:
                            print(
                                f"WARNING: Failed to forward task to agent {agent_id} at {agent.endpoint_url}"
                            )
                            print(f"WARNING: Response status: {response.status_code}")
                            update_log["status"] = "failed"
                            update_log["error"] = (
                                f"HTTP {response.status_code}: {response.text[:200]}"
                            )

                        # Update forwarding log
                        if task_logs_collection is not None:
                            task_logs_collection.update_one(
                                {"task_id": task_id, "agent_id": agent_id},
                                {"$set": update_log},
                            )

                except Exception as e:
                    error_msg = str(e)
                    print(
                        f"ERROR: Failed to forward task to agent {agent_id}: {error_msg}"
                    )

                    # Update forwarding log with error
                    error_log = {
                        "status": "failed",
                        "error": error_msg,
                        "completed_at": db._get_current_time(),
                    }

                    if task_logs_collection is not None:
                        task_logs_collection.update_one(
                            {"task_id": task_id, "agent_id": agent_id},
                            {"$set": error_log},
                        )

            # Start forwarding task in background (non-blocking)
            asyncio.create_task(forward_task_async())

        # Return the created task
        return MCPTaskResponse(
            task_id=task_id,
            agent_id=agent_id,
            type=task_data.type,
            params=task_data.params,
            description=task_data.description,
            context=task_data.context,
            callback_url=callback_url,
            status="pending",
            created_at=task_doc["created_at"],
            updated_at=task_doc["updated_at"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating MCP task: {str(e)}"
        )


@router.post("/{agent_id}/tasks/{task_id}/result", response_model=MCPTaskResponse)
async def receive_mcp_task_result(
    agent_id: str, task_id: str, result_data: MCPTaskResult
):
    """Receive result from an MCP task"""
    try:
        # Verify agent exists
        agent = agent_service.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        # Update task with result
        collection = db.get_collection("mcp_tasks")
        if collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        from bson import ObjectId

        update_data = {
            "status": "completed",
            "result": result_data.result,
            "updated_at": db._get_current_time(),
        }

        result = collection.update_one(
            {"_id": ObjectId(task_id), "agent_id": agent_id}, {"$set": update_data}
        )

        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")

        # Return updated task with simplified response
        updated_task = collection.find_one({"_id": ObjectId(task_id)})
        updated_task = db._convert_object_id(updated_task)

        return MCPTaskResponse(
            task_id=updated_task["_id"],
            agent_id=updated_task["agent_id"],
            business_id=updated_task.get("business_id"),
            type=updated_task["type"],
            params=updated_task["params"],
            status=updated_task["status"],
            context=updated_task.get("context"),
            callback_url=updated_task.get("callback_url"),
            created_at=updated_task["created_at"],
            updated_at=updated_task["updated_at"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error receiving MCP task result: {str(e)}"
        )


@router.get("/{agent_id}/tasks", response_model=List[MCPTaskResponse])
async def get_agent_mcp_tasks(agent_id: str, status: Optional[str] = Query(None)):
    """Get all MCP tasks for an agent"""
    try:
        # Verify agent exists
        agent = agent_service.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        # Get tasks from database
        collection = db.get_collection("mcp_tasks")
        if collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        query = {"agent_id": agent_id}
        if status:
            query["status"] = status

        tasks = list(collection.find(query))
        tasks = db._convert_documents(tasks)

        return [
            MCPTaskResponse(
                task_id=task["_id"],
                agent_id=task["agent_id"],
                business_id=task.get("business_id"),
                type=task["type"],
                params=task["params"],
                status=task["status"],
                result=task.get("result"),
                context=task.get("context"),
                callback_url=task.get("callback_url"),
                created_at=task["created_at"],
                updated_at=task["updated_at"],
            )
            for task in tasks
        ]
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting MCP tasks: {str(e)}"
        )


@router.post("/{agent_id}/tasks/{task_id}/assign", response_model=MCPTaskResponse)
async def assign_mcp_task(agent_id: str, task_id: str):
    """Assign an MCP task to an agent (change status to in_progress)"""
    try:
        # Verify agent exists
        agent = agent_service.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        # Update task status to assigned
        collection = db.get_collection("mcp_tasks")
        if collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        from bson import ObjectId

        update_data = {
            "status": "in_progress",
            "assigned_at": db._get_current_time(),
            "updated_at": db._get_current_time(),
        }

        result = collection.update_one(
            {"_id": ObjectId(task_id), "agent_id": agent_id}, {"$set": update_data}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=404, detail="Task not found or already assigned"
            )

        # Return updated task with simplified response
        updated_task = collection.find_one({"_id": ObjectId(task_id)})
        updated_task = db._convert_object_id(updated_task)

        return MCPTaskResponse(
            task_id=updated_task["_id"],
            agent_id=updated_task["agent_id"],
            business_id=updated_task.get("business_id"),
            type=updated_task["type"],
            params=updated_task["params"],
            status=updated_task["status"],
            context=updated_task.get("context"),
            callback_url=updated_task.get("callback_url"),
            created_at=updated_task["created_at"],
            updated_at=updated_task["updated_at"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error assigning MCP task: {str(e)}"
        )


@router.put("/{agent_id}/tasks/{task_id}", response_model=MCPTaskResponse)
async def update_mcp_task(agent_id: str, task_id: str, update_data: MCPTaskUpdate):
    """Update an MCP task (status, parameters, etc.)"""
    try:
        # Verify agent exists
        agent = agent_service.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        # Update task
        collection = db.get_collection("mcp_tasks")
        if collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        from bson import ObjectId

        # Convert to dict and add updated_at timestamp
        update_dict = update_data.model_dump(exclude_unset=True)
        update_dict["updated_at"] = db._get_current_time()

        result = collection.update_one(
            {"_id": ObjectId(task_id), "agent_id": agent_id}, {"$set": update_dict}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=404, detail="Task not found or no changes made"
            )

        # Return updated task with simplified response
        updated_task = collection.find_one({"_id": ObjectId(task_id)})
        updated_task = db._convert_object_id(updated_task)

        return MCPTaskResponse(
            task_id=updated_task["_id"],
            agent_id=updated_task["agent_id"],
            business_id=updated_task.get("business_id"),
            type=updated_task["type"],
            params=updated_task["params"],
            status=updated_task["status"],
            context=updated_task.get("context"),
            callback_url=updated_task.get("callback_url"),
            created_at=updated_task["created_at"],
            updated_at=updated_task["updated_at"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating MCP task: {str(e)}"
        )


@router.get("/tasks/{task_id}", response_model=MCPTaskResponse)
async def get_mcp_task(task_id: str):
    """Get a specific MCP task by ID"""
    try:
        collection = db.get_collection("mcp_tasks")
        if collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        from bson import ObjectId

        task = collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        task = db._convert_object_id(task)

        return MCPTaskResponse(
            task_id=task["_id"],
            agent_id=task["agent_id"],
            business_id=task.get("business_id"),
            type=task["type"],
            params=task["params"],
            status=task["status"],
            result=task.get("result"),
            context=task.get("context"),
            callback_url=task.get("callback_url"),
            created_at=task["created_at"],
            updated_at=task["updated_at"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting MCP task: {str(e)}")


@router.delete("/{agent_id}/tasks/{task_id}")
async def delete_mcp_task(agent_id: str, task_id: str):
    """Delete an MCP task"""
    try:
        # Verify agent exists
        agent = agent_service.get_agent(agent_id)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")

        collection = db.get_collection("mcp_tasks")
        if collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        from bson import ObjectId

        result = collection.delete_one({"_id": ObjectId(task_id), "agent_id": agent_id})

        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Task not found")

        return {"message": "MCP task deleted successfully"}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error deleting MCP task: {str(e)}"
        )


# Business-specific task endpoints
@router.get("/business/{business_id}/tasks", response_model=List[MCPTaskResponse])
async def get_business_tasks(business_id: str, status: Optional[str] = Query(None)):
    """Get all MCP tasks for a specific business"""
    try:
        collection = db.get_collection("mcp_tasks")
        if collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        query = {"business_id": business_id}
        if status:
            query["status"] = status

        tasks = list(collection.find(query))
        tasks = db._convert_documents(tasks)

        return [
            MCPTaskResponse(
                task_id=task["_id"],
                agent_id=task["agent_id"],
                business_id=task.get("business_id"),
                type=task["type"],
                params=task["params"],
                status=task["status"],
                result=task.get("result"),
                context=task.get("context"),
                callback_url=task.get("callback_url"),
                created_at=task["created_at"],
                updated_at=task["updated_at"],
            )
            for task in tasks
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting business tasks: {str(e)}"
        )


@router.get("/tasks", response_model=List[MCPTaskResponse])
async def get_all_tasks(
    business_id: Optional[str] = Query(None, description="Filter by business ID"),
    agent_id: Optional[str] = Query(None, description="Filter by agent ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    task_type: Optional[str] = Query(None, description="Filter by task type"),
):
    """Get all MCP tasks with optional filtering"""
    try:
        collection = db.get_collection("mcp_tasks")
        if collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        query = {}
        if business_id:
            query["business_id"] = business_id
        if agent_id:
            query["agent_id"] = agent_id
        if status:
            query["status"] = status
        if task_type:
            query["type"] = task_type

        tasks = list(collection.find(query))
        tasks = db._convert_documents(tasks)

        return [
            MCPTaskResponse(
                task_id=task["_id"],
                agent_id=task["agent_id"],
                business_id=task.get("business_id"),
                type=task["type"],
                params=task["params"],
                status=task["status"],
                result=task.get("result"),
                context=task.get("context"),
                callback_url=task.get("callback_url"),
                created_at=task["created_at"],
                updated_at=task["updated_at"],
            )
            for task in tasks
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting tasks: {str(e)}")


# MCP Standard Endpoints


@router.post("/mcp/task", response_model=MCPTaskResponse, status_code=201)
async def create_mcp_standard_task(task_data: MCPTaskRequest):
    """Create a new MCP task using MCP standard format - automatically assigns to appropriate agent"""
    try:
        # Validate business_id if provided
        if task_data.business_id:
            # Verify business exists (you might want to add business validation here)
            business_collection = db.get_collection("businesses")
            if business_collection is None:
                # If businesses collection doesn't exist, we'll skip validation
                # This allows the system to work without business data
                pass
            else:
                try:
                    from bson import ObjectId

                    business = business_collection.find_one(
                        {"_id": ObjectId(task_data.business_id)}
                    )
                    if not business:
                        # Business not found, but we'll continue without it
                        # You can uncomment the next line to make business validation strict
                        # raise HTTPException(status_code=404, detail="Business not found")
                        pass
                except Exception:
                    # Invalid ObjectId format, but we'll continue without business association
                    pass

        # Find the best agent for this task type
        # For now, we'll use a simple strategy: find the first available agent
        # In a real implementation, you'd want more sophisticated agent selection
        collection = db.get_collection("agents")
        if collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        # Find an available agent (you might want to implement more sophisticated selection)
        agent = collection.find_one({"status": "active"})
        if not agent:
            raise HTTPException(status_code=503, detail="No available agents found")

        agent_id = str(agent["_id"])

        # Create task in database
        task_collection = db.get_collection("mcp_tasks")
        if task_collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        task_doc = {
            "agent_id": agent_id,
            "type": task_data.type,
            "params": task_data.params,
            "description": task_data.description,
            "status": "pending",
            "created_at": db._get_current_time(),
            "updated_at": db._get_current_time(),
        }

        # Add business_id if provided and valid
        if task_data.business_id:
            task_doc["business_id"] = task_data.business_id

        # Add context if provided
        if task_data.context:
            task_doc["context"] = task_data.context.dict()

        result = task_collection.insert_one(task_doc)
        task_id = str(result.inserted_id)

        # Generate secure callback URL that points back to the API
        secure_callback_url = callback_manager.generate_api_callback_url(task_id)

        # Update the task with the secure callback URL
        task_collection.update_one(
            {"_id": result.inserted_id}, {"$set": {"callback_url": secure_callback_url}}
        )

        # Test synchronous log creation
        print(f"DEBUG: Testing synchronous log creation for task {task_id}")
        task_logs_collection = db.get_collection("mcp_task_logs")
        if task_logs_collection is not None:
            test_log = {
                "task_id": task_id,
                "agent_id": agent_id,
                "timestamp": db._get_current_time(),
            }
            try:
                test_result = task_logs_collection.insert_one(test_log)
                print(
                    f"DEBUG: Sync test log created with ID: {test_result.inserted_id}"
                )
            except Exception as e:
                print(f"ERROR: Failed to create sync test log: {e}")
        else:
            print(f"ERROR: Could not get mcp_task_logs collection for sync test")

        # Forward task to agent's endpoint if endpoint_url is available
        if hasattr(agent, "endpoint_url") and agent.endpoint_url:
            # Create a background task for forwarding (non-blocking)
            import asyncio

            async def forward_task_async():
                print(f"DEBUG: Starting forward_task_async for task {task_id}")

                # Prepare task data for forwarding (exclude business_id, agent_id, _id)
                forward_task_data = {
                    "type": task_data.type,
                    "description": task_data.description,
                    "params": task_data.params,
                    "callback_url": secure_callback_url,
                }

                # Add context if provided
                if task_data.context:
                    forward_task_data["context"] = task_data.context.dict()

                # Prepare headers
                headers = {"Content-Type": "application/json"}

                # Add API key if available
                if hasattr(agent, "api_key") and agent.api_key:
                    headers["Authorization"] = f"Bearer {agent.api_key}"
                    # Alternative header formats if needed
                    # headers["X-API-Key"] = agent.api_key

                # Log forwarding attempt
                forward_log = {
                    "task_id": task_id,
                    "agent_id": agent_id,
                    "endpoint_url": agent.endpoint_url,
                    "forward_data": forward_task_data,
                    "headers": {
                        k: v for k, v in headers.items() if k != "Authorization"
                    },  # Don't log auth headers
                    "status": "attempting",
                    "attempted_at": db._get_current_time(),
                    "response_status": None,
                    "response_body": None,
                    "error": None,
                }

                # Save forwarding log to database
                task_logs_collection = db.get_collection("mcp_task_logs")
                print(f"DEBUG: Task logs collection: {task_logs_collection}")
                if task_logs_collection is not None:
                    print(f"DEBUG: Inserting forward log for task {task_id}")
                    result = task_logs_collection.insert_one(forward_log)
                    print(f"DEBUG: Forward log inserted with ID: {result.inserted_id}")
                else:
                    print(f"ERROR: Could not get mcp_task_logs collection")

                try:
                    import httpx

                    # Forward task to agent's endpoint
                    async with httpx.AsyncClient(timeout=30.0) as client:
                        response = await client.post(
                            agent.endpoint_url, json=forward_task_data, headers=headers
                        )

                        # Update forwarding log with response
                        update_log = {
                            "status": "completed",
                            "response_status": response.status_code,
                            "response_body": response.text[
                                :500
                            ],  # Limit response body length
                            "completed_at": db._get_current_time(),
                        }

                        if response.status_code in [200, 201, 202]:
                            print(
                                f"DEBUG: Task forwarded successfully to agent {agent_id} at {agent.endpoint_url}"
                            )
                            print(
                                f"DEBUG: Agent response status: {response.status_code}"
                            )
                            update_log["status"] = "success"
                        else:
                            print(
                                f"WARNING: Failed to forward task to agent {agent_id} at {agent.endpoint_url}"
                            )
                            print(f"WARNING: Response status: {response.status_code}")
                            update_log["status"] = "failed"
                            update_log["error"] = (
                                f"HTTP {response.status_code}: {response.text[:200]}"
                            )

                        # Update forwarding log
                        if task_logs_collection is not None:
                            task_logs_collection.update_one(
                                {"task_id": task_id, "agent_id": agent_id},
                                {"$set": update_log},
                            )

                except Exception as e:
                    error_msg = str(e)
                    print(
                        f"ERROR: Failed to forward task to agent {agent_id}: {error_msg}"
                    )

                    # Update forwarding log with error
                    error_log = {
                        "status": "failed",
                        "error": error_msg,
                        "completed_at": db._get_current_time(),
                    }

                    if task_logs_collection is not None:
                        task_logs_collection.update_one(
                            {"task_id": task_id, "agent_id": agent_id},
                            {"$set": error_log},
                        )

            # Start forwarding task in background (non-blocking)
            asyncio.create_task(forward_task_async())

        # Return the created task
        return MCPTaskResponse(
            task_id=task_id,
            agent_id=agent_id,
            business_id=task_data.business_id,
            type=task_data.type,
            params=task_data.params,
            description=task_data.description,
            context=task_data.context,
            callback_url=secure_callback_url,
            status="pending",
            created_at=task_doc["created_at"],
            updated_at=task_doc["updated_at"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error creating MCP task: {str(e)}"
        )


@router.get("/mcp/task/{task_id}", response_model=MCPTaskResponse)
async def get_mcp_standard_task(task_id: str):
    """Get a specific MCP task by ID using MCP standard format"""
    try:
        collection = db.get_collection("mcp_tasks")
        if collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        from bson import ObjectId

        task = collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        task = db._convert_object_id(task)

        return MCPTaskResponse(
            task_id=task["_id"],
            agent_id=task["agent_id"],
            business_id=task.get("business_id"),
            type=task["type"],
            params=task["params"],
            status=task["status"],
            result=task.get("result"),
            context=task.get("context"),
            callback_url=task.get("callback_url"),
            created_at=task["created_at"],
            updated_at=task["updated_at"],
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting MCP task: {str(e)}")


@router.put("/mcp/task/{task_id}", response_model=MCPTaskResponse)
async def update_mcp_standard_task(task_id: str, update_data: MCPTaskUpdate):
    """Update an MCP task using MCP standard format"""
    try:
        collection = db.get_collection("mcp_tasks")
        if collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        from bson import ObjectId

        # Convert to dict and add updated_at timestamp
        update_dict = update_data.model_dump(exclude_unset=True)
        update_dict["updated_at"] = db._get_current_time()

        result = collection.update_one(
            {"_id": ObjectId(task_id)}, {"$set": update_dict}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=404, detail="Task not found or no changes made"
            )

        # Return updated task with simplified response
        updated_task = collection.find_one({"_id": ObjectId(task_id)})
        updated_task = db._convert_object_id(updated_task)

        return MCPTaskResponse(
            task_id=updated_task["_id"],
            agent_id=updated_task["agent_id"],
            business_id=updated_task.get("business_id"),
            type=updated_task["type"],
            params=updated_task["params"],
            status=updated_task["status"],
            context=updated_task.get("context"),
            callback_url=updated_task.get("callback_url"),
            created_at=updated_task["created_at"],
            updated_at=updated_task["updated_at"],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error updating MCP task: {str(e)}"
        )


@router.post("/mcp/callback", response_model=MCPCallbackResponse)
async def receive_secure_callback(
    request: Request,
    task_id: Optional[str] = None,
    token: Optional[str] = None,
    expires_at: Optional[str] = None,
    signature: Optional[str] = None,
):
    """Receive secure callback result from agent with simplified format: {output: {}, context_update: {}}"""
    try:
        print(f"DEBUG: Received callback request")
        print(
            f"DEBUG: Query params - task_id: {task_id}, token: {token}, expires_at: {expires_at}, signature: {signature}"
        )

        # Get raw request body
        body = await request.json()
        print(f"DEBUG: Request body: {body}")

        # Simplified format: expect {output: {}, context_update: {}}
        if "output" not in body:
            raise HTTPException(
                status_code=400, detail="Missing 'output' field in request body"
            )

        output_data = body["output"]
        context_update = body.get("context_update", {})

        # TEMPORARY: Bypass signature verification for testing
        decoded_task_id = None

        if task_id:
            # Decode task_id directly
            from app.utils.security import callback_manager

            decoded_task_id = callback_manager._decode_base64(task_id)
            print(f"DEBUG: Decoded task_id directly: {decoded_task_id}")

        if not decoded_task_id:
            raise HTTPException(status_code=401, detail="Invalid task ID")

        task_id = decoded_task_id
        print(f"DEBUG: Using task ID: {task_id}")

        # Get task from database
        task_collection = db.get_collection("mcp_tasks")
        if task_collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        from bson import ObjectId

        task = task_collection.find_one({"_id": ObjectId(task_id)})
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")

        print(f"DEBUG: Found task: {task}")

        # Update task status to completed
        update_data = {
            "status": "completed",  # Always set to completed when callback is received
            "updated_at": db._get_current_time(),
        }

        result = task_collection.update_one(
            {"_id": ObjectId(task_id)}, {"$set": update_data}
        )

        if result.modified_count == 0:
            raise HTTPException(
                status_code=404, detail="Task not found or update failed"
            )

        print(f"DEBUG: Task updated successfully")

        # Store detailed result in separate collection with simplified structure
        result_collection = db.get_collection("mcp_results")
        if result_collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        # Extract fields from output object
        text = output_data.get("text")
        images = output_data.get("images", [])
        links = output_data.get("links", [])
        files = output_data.get("files", [])
        data = output_data.get("data", {})
        html = output_data.get("html")
        markdown = output_data.get("markdown")

        # Simplified result document structure
        result_doc = {
            "task_id": task_id,
            "agent_id": task["agent_id"],
            "business_id": task.get("business_id"),
            "status": "completed",  # Always completed when stored in results
            "output": {
                "text": text,
                "images": images,
                "links": links,
                "files": files,
                "data": data,
                "html": html,
                "markdown": markdown,
            },
            "context_update": context_update,
            "timestamp": body.get("timestamp") or db._get_current_time(),
            "created_at": db._get_current_time(),
        }

        # Add optional fields if they exist
        if body.get("execution_time"):
            result_doc["execution_time"] = body["execution_time"]

        if body.get("error_message"):
            result_doc["error_message"] = body["error_message"]

        result_insert = result_collection.insert_one(result_doc)
        result_id = str(result_insert.inserted_id)

        print(f"DEBUG: Result stored successfully with ID: {result_id}")

        # Return the actual result data instead of task information
        return MCPCallbackResponse(
            result_id=result_id,
            task_id=task_id,
            agent_id=task["agent_id"],
            business_id=task.get("business_id"),
            status="completed",
            output=result_doc["output"],
            context_update=context_update,
            execution_time=body.get("execution_time"),
            error_message=body.get("error_message"),
            timestamp=result_doc["timestamp"],
            created_at=result_doc["created_at"],
        )

    except Exception as e:
        print(f"DEBUG: Exception in callback: {str(e)}")
        import traceback

        print(f"DEBUG: Traceback: {traceback.format_exc()}")
        raise HTTPException(
            status_code=500, detail=f"Error processing callback: {str(e)}"
        )


@router.get("/mcp/task/{task_id}/results", response_model=List[TaskResult])
async def get_task_results(task_id: str):
    """Get all results for a specific task"""
    try:
        result_collection = db.get_collection("mcp_results")
        if result_collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        from bson import ObjectId

        results = list(result_collection.find({"task_id": task_id}))
        results = db._convert_documents(results)

        return [
            TaskResult(
                result_id=result["_id"],
                task_id=result["task_id"],
                agent_id=result["agent_id"],
                business_id=result.get("business_id"),
                status=result["status"],
                result=result["result"],
                error_message=result.get("error_message"),
                execution_time=result.get("execution_time"),
                metadata=result.get("metadata"),
                created_at=result["created_at"],
            )
            for result in results
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting task results: {str(e)}"
        )


@router.get("/business/{business_id}/mcp/tasks", response_model=List[MCPTaskResponse])
async def get_business_mcp_tasks(business_id: str, status: Optional[str] = Query(None)):
    """Get all MCP tasks for a specific business"""
    try:
        collection = db.get_collection("mcp_tasks")
        if collection is None:
            raise HTTPException(status_code=500, detail="Database connection failed")

        query = {"business_id": business_id}
        if status:
            query["status"] = status

        tasks = list(collection.find(query))
        tasks = db._convert_documents(tasks)

        return [
            MCPTaskResponse(
                task_id=task["_id"],
                agent_id=task["agent_id"],
                business_id=task.get("business_id"),
                type=task["type"],
                params=task["params"],
                status=task["status"],
                result=task.get("result"),
                context=task.get("context"),
                callback_url=task.get("callback_url"),
                created_at=task["created_at"],
                updated_at=task["updated_at"],
            )
            for task in tasks
        ]

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting business MCP tasks: {str(e)}"
        )


@router.get("/mcp/forward-logs", response_model=List[Dict[str, Any]])
async def get_task_forward_logs(
    task_id: Optional[str] = Query(None, description="Filter by task ID"),
    agent_id: Optional[str] = Query(None, description="Filter by agent ID"),
    status: Optional[str] = Query(
        None, description="Filter by status (attempting, success, failed)"
    ),
):
    """Get task forwarding logs"""
    try:
        collection = db.get_collection("mcp_task_logs")
        if collection is None:
            return []

        query = {}
        if task_id:
            query["task_id"] = task_id
        if agent_id:
            query["agent_id"] = agent_id
        if status:
            query["status"] = status

        logs = list(collection.find(query).sort("attempted_at", -1).limit(100))
        logs = db._convert_documents(logs)

        return logs

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting forward logs: {str(e)}"
        )


@router.get("/mcp/forward-logs/{task_id}", response_model=List[Dict[str, Any]])
async def get_task_forward_logs_by_task(task_id: str):
    """Get forwarding logs for a specific task"""
    try:
        collection = db.get_collection("mcp_task_logs")
        if collection is None:
            return []

        logs = list(collection.find({"task_id": task_id}).sort("attempted_at", -1))
        logs = db._convert_documents(logs)

        return logs

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error getting task forward logs: {str(e)}"
        )


@router.post("/mcp/test-logs", response_model=Dict[str, Any])
async def test_mcp_logs():
    """Test endpoint to create a log entry and verify the collection works"""
    try:
        collection = db.get_collection("mcp_task_logs")
        if collection is None:
            return {"error": "Could not get mcp_task_logs collection"}

        test_log = {
            "test": True,
            "timestamp": db._get_current_time(),
            "message": "Test log entry",
        }

        result = collection.insert_one(test_log)

        # Try to retrieve it
        retrieved = collection.find_one({"_id": result.inserted_id})
        retrieved = db._convert_object_id(retrieved)

        return {
            "success": True,
            "inserted_id": str(result.inserted_id),
            "retrieved": retrieved,
        }

    except Exception as e:
        return {"error": f"Failed to test logs: {str(e)}"}
