import os
from dotenv import load_dotenv

# Load environment variables first
load_dotenv()

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import httpx
import asyncio
import json
from datetime import datetime

# Import database module
try:
    from app.api.v0.database import db

    DATABASE_AVAILABLE = True
except ImportError:
    DATABASE_AVAILABLE = False
    print("⚠️ Database module not available. Business data will not be saved.")

# Import task automation system
try:
    from app.api.v0.task_automation import automation_engine

    AUTOMATION_AVAILABLE = True
    print("✅ Task automation module loaded successfully.")
except ImportError:
    AUTOMATION_AVAILABLE = False
    print(
        "⚠️ Task automation module not available. Automated tasks will not be created."
    )

app = FastAPI(title="Multi-Agent Business Analysis System", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


# Business input model
class BusinessInput(BaseModel):
    business_name: str
    business_type: str  # e.g., "coffee_shop", "restaurant", "retail_store", "tech_startup", "consulting_firm"
    location: str
    description: str  # Brief description of the business
    target_market: str  # Description of target customers
    competitors: List[str]
    growth_goals: List[str]
    initial_investment: Optional[float] = None  # In local currency
    team_size: Optional[int] = None
    unique_value_proposition: Optional[str] = None
    business_model: Optional[str] = (
        None  # e.g., "b2c", "b2b", "marketplace", "subscription"
    )
    industry: Optional[str] = (
        None  # e.g., "food_beverage", "technology", "retail", "services"
    )
    market_size: Optional[str] = (
        None  # e.g., "local", "regional", "national", "international"
    )
    technology_requirements: Optional[List[str]] = None
    regulatory_requirements: Optional[List[str]] = None


# External Agent models
class ExternalAgentRegister(BaseModel):
    agent_name: str
    agent_type: str  # e.g., "custom_analytics", "specialized_financial", "market_research"
    description: str
    capabilities: List[str]  # List of capabilities this agent provides
    endpoint_url: str  # The URL where this agent can be reached
    callback_url: Optional[str] = None  # URL for receiving results from this agent
    api_key: Optional[str] = None  # Optional API key for authentication
    status: Optional[str] = "active"  # active, inactive, maintenance
    version: Optional[str] = "1.0.0"
    contact_info: Optional[Dict[str, str]] = None  # email, phone, etc.
    configuration: Optional[Dict[str, Any]] = None  # Any additional configuration
    mcp_support: Optional[bool] = False  # Whether this agent supports MCP protocol


class ExternalAgentUpdate(BaseModel):
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


# MCP Task Management Models
class MCPTaskRequest(BaseModel):
    description: str
    task_type: str  # e.g., "content_generation", "analysis", "prediction"
    parameters: Dict[str, Any]
    context: Optional[Dict[str, Any]] = None
    callback_url: Optional[str] = None
    priority: Optional[str] = "normal"  # low, normal, high, urgent
    timeout_seconds: Optional[int] = 300  # 5 minutes default


class MCPTaskResponse(BaseModel):
    task_id: str
    status: str  # pending, in_progress, completed, failed
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    created_at: str
    estimated_completion: Optional[str] = None


class MCPResult(BaseModel):
    task_id: str
    agent_id: str
    status: str  # success, failed, partial
    result: Dict[str, Any]
    error_message: Optional[str] = None
    execution_time: Optional[float] = None
    timestamp: str


# Response model
class BusinessAnalysisResponse(BaseModel):
    business_name: str
    timestamp: str
    business_id: Optional[str] = None  # Add business ID field
    strategic_plan: Dict[str, Any]
    creative_analysis: Dict[str, Any]
    financial_analysis: Dict[str, Any]
    sales_strategy: Dict[str, Any]
    swot_analysis: Dict[str, Any]
    business_model_canvas: Dict[str, Any]
    analytics_summary: Dict[str, Any]
    overall_recommendations: List[str]


# Task and Goal models for automation
class TaskCreate(BaseModel):
    business_name: str
    agent_type: str
    task_type: str
    frequency: str
    parameters: Optional[Dict[str, Any]] = {}
    status: Optional[str] = "pending"


class TaskUpdate(BaseModel):
    status: Optional[str] = None
    results: Optional[Dict[str, Any]] = None
    last_executed: Optional[str] = None
    next_execution: Optional[str] = None
    parameters: Optional[Dict[str, Any]] = None


class GoalCreate(BaseModel):
    goal_type: str
    target_value: float
    current_value: Optional[float] = 0
    deadline: str
    status: Optional[str] = "on_track"


class GoalUpdate(BaseModel):
    current_value: Optional[float] = None
    status: Optional[str] = None
    target_value: Optional[float] = None
    deadline: Optional[str] = None


# Agent configuration
AGENT_CONFIG = {
    "strategic": {"url": "http://localhost:5001", "port": 5001},
    "creative": {"url": "http://localhost:5002", "port": 5002},
    "financial": {"url": "http://localhost:5003", "port": 5003},
    "sales": {"url": "http://localhost:5004", "port": 5004},
    "manager": {"url": "http://localhost:5005", "port": 5005},
    "analytics": {"url": "http://localhost:5006", "port": 5006},
    "swot": {"url": "http://localhost:5007", "port": 5007},
    "business_model": {"url": "http://localhost:5008", "port": 5008},
}


class MCPClient:
    """MCP Client for communicating with agent servers"""

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)

    async def send_message(
        self, agent_url: str, message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send message to agent via MCP"""
        try:
            response = await self.client.post(
                f"{agent_url}/receive_message",
                json=message,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to communicate with agent: {str(e)}"
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Agent error: {e.response.text}",
            )


class CoreAgent:
    """Core Agent that orchestrates the multi-agent system"""

    def __init__(self):
        self.mcp_client = MCPClient()

    async def process_business_request(
        self, business_data: BusinessInput
    ) -> BusinessAnalysisResponse:
        """Main processing logic for business analysis"""

        # Step 1: Send to Strategic Agent
        strategic_message = {
            "agent_type": "strategic",
            "business_data": business_data.model_dump(),
            "timestamp": datetime.now().isoformat(),
            "request_id": f"req_{datetime.now().timestamp()}",
        }

        strategic_response = await self.mcp_client.send_message(
            AGENT_CONFIG["strategic"]["url"], strategic_message
        )

        # Step 2: Send to SWOT Agent (can run in parallel with other agents)
        swot_message = {
            "agent_type": "swot",
            "business_data": business_data.model_dump(),
            "strategic_plan": strategic_response.get("strategic_plan", {}),
            "timestamp": datetime.now().isoformat(),
            "request_id": f"req_{datetime.now().timestamp()}",
        }

        swot_response = await self.mcp_client.send_message(
            AGENT_CONFIG["swot"]["url"], swot_message
        )

        # Step 3: Send to Business Model Canvas Agent (uses SWOT analysis)
        bmc_message = {
            "agent_type": "business_model",
            "business_data": business_data.model_dump(),
            "strategic_plan": strategic_response.get("strategic_plan", {}),
            "swot_analysis": swot_response.get("swot_analysis", {}),
            "timestamp": datetime.now().isoformat(),
            "request_id": f"req_{datetime.now().timestamp()}",
        }

        bmc_response = await self.mcp_client.send_message(
            AGENT_CONFIG["business_model"]["url"], bmc_message
        )

        # Step 4: Send to other agents in parallel
        agent_tasks = []

        # Creative Agent
        creative_message = {
            "agent_type": "creative",
            "business_data": business_data.model_dump(),
            "strategic_plan": strategic_response.get("strategic_plan", {}),
            "timestamp": datetime.now().isoformat(),
            "request_id": f"req_{datetime.now().timestamp()}",
        }
        agent_tasks.append(
            self.mcp_client.send_message(
                AGENT_CONFIG["creative"]["url"], creative_message
            )
        )

        # Financial Agent
        financial_message = {
            "agent_type": "financial",
            "business_data": business_data.model_dump(),
            "strategic_plan": strategic_response.get("strategic_plan", {}),
            "timestamp": datetime.now().isoformat(),
            "request_id": f"req_{datetime.now().timestamp()}",
        }
        agent_tasks.append(
            self.mcp_client.send_message(
                AGENT_CONFIG["financial"]["url"], financial_message
            )
        )

        # Sales Agent
        sales_message = {
            "agent_type": "sales",
            "business_data": business_data.model_dump(),
            "strategic_plan": strategic_response.get("strategic_plan", {}),
            "timestamp": datetime.now().isoformat(),
            "request_id": f"req_{datetime.now().timestamp()}",
        }
        agent_tasks.append(
            self.mcp_client.send_message(AGENT_CONFIG["sales"]["url"], sales_message)
        )

        # Execute all agent tasks in parallel
        agent_responses = await asyncio.gather(*agent_tasks)
        creative_response, financial_response, sales_response = agent_responses

        # Step 5: Trigger Analytics with all data
        analytics_message = {
            "agent_type": "analytics",
            "business_data": business_data.model_dump(),
            "strategic_plan": strategic_response.get("strategic_plan", {}),
            "creative_analysis": creative_response.get("creative_analysis", {}),
            "financial_analysis": financial_response.get("financial_analysis", {}),
            "sales_strategy": sales_response.get("sales_strategy", {}),
            "swot_analysis": swot_response.get("swot_analysis", {}),
            "business_model_canvas": bmc_response.get("business_model_canvas", {}),
            "timestamp": datetime.now().isoformat(),
            "request_id": f"req_{datetime.now().timestamp()}",
        }

        analytics_response = await self.mcp_client.send_message(
            AGENT_CONFIG["analytics"]["url"], analytics_message
        )

        # Step 6: Generate overall recommendations
        overall_recommendations = self._generate_overall_recommendations(
            strategic_response,
            creative_response,
            financial_response,
            sales_response,
            swot_response,
            bmc_response,
            analytics_response,
        )

        # Step 7: Return aggregated response
        return BusinessAnalysisResponse(
            business_name=business_data.business_name,
            timestamp=datetime.now().isoformat(),
            business_id=None,  # Will be set after database save
            strategic_plan=strategic_response.get("strategic_plan", {}),
            creative_analysis=creative_response.get("creative_analysis", {}),
            financial_analysis=financial_response.get("financial_analysis", {}),
            sales_strategy=sales_response.get("sales_strategy", {}),
            swot_analysis=swot_response.get("swot_analysis", {}),
            business_model_canvas=bmc_response.get("business_model_canvas", {}),
            analytics_summary=analytics_response.get("analytics_summary", {}),
            overall_recommendations=overall_recommendations,
        )

    def _generate_overall_recommendations(
        self, strategic, creative, financial, sales, swot, bmc, analytics
    ):
        """Generate overall recommendations based on all agent outputs"""
        recommendations = []

        # Add strategic recommendations
        if strategic.get("strategic_plan", {}).get("key_recommendations"):
            recommendations.extend(strategic["strategic_plan"]["key_recommendations"])

        # Add creative recommendations
        if creative.get("creative_analysis", {}).get("recommendations"):
            recommendations.extend(creative["creative_analysis"]["recommendations"])

        # Add financial recommendations
        if financial.get("financial_analysis", {}).get("recommendations"):
            recommendations.extend(financial["financial_analysis"]["recommendations"])

        # Add sales recommendations
        if sales.get("sales_strategy", {}).get("recommendations"):
            recommendations.extend(sales["sales_strategy"]["recommendations"])

        # Add SWOT action plan
        if (
            swot.get("swot_analysis", {})
            .get("action_plan", {})
            .get("immediate_actions")
        ):
            recommendations.extend(
                swot["swot_analysis"]["action_plan"]["immediate_actions"]
            )

        # Add Business Model Canvas insights
        if (
            bmc.get("business_model_canvas", {})
            .get("canvas_insights", {})
            .get("strategic_recommendations")
        ):
            recommendations.extend(
                bmc["business_model_canvas"]["canvas_insights"][
                    "strategic_recommendations"
                ]
            )

        # Add analytics insights
        if analytics.get("analytics_summary", {}).get("key_insights"):
            recommendations.extend(analytics["analytics_summary"]["key_insights"])

        return list(set(recommendations))  # Remove duplicates


# Initialize core agent
core_agent = CoreAgent()


@app.post("/process-business", response_model=BusinessAnalysisResponse)
async def process_business(business_input: BusinessInput):
    """
    Process business analysis request through multi-agent system
    """
    try:
        result = await core_agent.process_business_request(business_input)

        # Save to database if available
        if DATABASE_AVAILABLE:
            try:
                business_id = db.save_business(
                    business_input.model_dump(), result.model_dump()
                )
                if business_id:
                    print(f"✅ Business saved to database with ID: {business_id}")
                    # Set the business ID in the response
                    result.business_id = business_id

                # Create automated tasks if automation is available
                if AUTOMATION_AVAILABLE:
                    try:
                        await automation_engine.create_business_automation(
                            business_id,
                            business_input.business_name,
                            business_input.business_type,
                        )
                        print(
                            f"✅ Automation tasks created for business: {business_id}"
                        )
                    except Exception as auto_error:
                        print(f"⚠️ Failed to create automation tasks: {auto_error}")

            except Exception as db_error:
                print(f"⚠️ Failed to save to database: {db_error}")

        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.get("/get-analysis/{business_id}")
async def get_analysis(business_id: str):
    """
    Get business analysis by ID
    """
    if not DATABASE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Database not available")

    try:
        business = db.get_business(business_id)
        analysis = db.get_analysis(business_id)

        if not business:
            raise HTTPException(status_code=404, detail="Business not found")

        if not analysis:
            raise HTTPException(status_code=404, detail="Analysis not found")

        return {"business": business, "analysis": analysis}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve analysis: {str(e)}"
        )


@app.get("/get-all-businesses")
async def get_all_businesses(limit: int = 50):
    """
    Get all businesses with their analysis
    """
    if not DATABASE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Database not available")

    try:
        businesses = db.get_all_businesses(limit)
        return {"businesses": businesses}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve businesses: {str(e)}"
        )


@app.get("/search-businesses")
async def search_businesses(q: str, business_type: str = None):
    """
    Search businesses by name, description, or industry
    """
    if not DATABASE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Database not available")

    try:
        businesses = db.search_businesses(q, business_type)
        return {"businesses": businesses}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to search businesses: {str(e)}"
        )


@app.delete("/delete-business/{business_id}")
async def delete_business(business_id: str):
    """
    Delete business and its analysis
    """
    if not DATABASE_AVAILABLE:
        raise HTTPException(status_code=503, detail="Database not available")

    try:
        success = db.delete_business(business_id)
        if not success:
            raise HTTPException(status_code=404, detail="Business not found")

        return {"message": "Business deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete business: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = "connected" if DATABASE_AVAILABLE and db.connect() else "disconnected"
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": db_status,
    }


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Multi-Agent Business Analysis System",
        "version": "1.0.1",
        "endpoints": {"process_business": "/process-business", "health": "/health"},
        "agents": {
            "strategic": "Port 5001",
            "creative": "Port 5002",
            "financial": "Port 5003",
            "sales": "Port 5004",
            "manager": "Port 5005",
            "analytics": "Port 5006",
            "swot": "Port 5007",
            "business_model": "Port 5008",
        },
    }


# Automation API endpoints
@app.get("/automation/summary")
async def get_automation_summary():
    """Get automation system summary"""
    if not AUTOMATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Automation system not available")

    return automation_engine.get_automation_summary()


@app.get("/automation/business/{business_id}/tasks")
async def get_business_tasks(business_id: str):
    """Get all automated tasks for a specific business"""
    if not AUTOMATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Automation system not available")

    tasks = automation_engine.get_business_tasks(business_id)
    return {
        "business_id": business_id,
        "tasks": tasks,
    }


@app.post("/automation/business/{business_id}/tasks")
async def create_business_task(business_id: str, task_data: TaskCreate):
    """Create a new automated task for a business"""
    if not AUTOMATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Automation system not available")

    try:
        # Convert Pydantic model to dict and add business_id
        task_dict = task_data.model_dump()
        task_dict["business_id"] = business_id

        # Save task to database
        task_id = db.save_task(task_dict)

        if task_id:
            return {
                "message": "Task created successfully",
                "task_id": task_id,
                "business_id": business_id,
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create task")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create task: {str(e)}")


@app.put("/automation/tasks/{task_id}")
async def update_task(task_id: str, update_data: TaskUpdate):
    """Update an existing task"""
    if not AUTOMATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Automation system not available")

    try:
        # Convert Pydantic model to dict, excluding None values
        update_dict = {
            k: v for k, v in update_data.model_dump().items() if v is not None
        }

        success = db.update_task(task_id, update_dict)

        if success:
            return {"message": "Task updated successfully", "task_id": task_id}
        else:
            raise HTTPException(status_code=404, detail="Task not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update task: {str(e)}")


@app.delete("/automation/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    if not AUTOMATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Automation system not available")

    try:
        success = db.delete_task(task_id)

        if success:
            return {"message": "Task deleted successfully", "task_id": task_id}
        else:
            raise HTTPException(status_code=404, detail="Task not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete task: {str(e)}")


@app.get("/automation/business/{business_id}/goals")
async def get_business_goals(business_id: str):
    """Get all goals for a specific business"""
    if not AUTOMATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Automation system not available")

    goals = automation_engine.get_business_goals(business_id)
    return {
        "business_id": business_id,
        "goals": goals,
    }


@app.post("/automation/business/{business_id}/goals")
async def create_business_goal(business_id: str, goal_data: GoalCreate):
    """Create a new goal for a business"""
    if not AUTOMATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Automation system not available")

    try:
        # Convert Pydantic model to dict and add business_id
        goal_dict = goal_data.model_dump()
        goal_dict["business_id"] = business_id

        # Save goal to database
        goal_id = db.save_goal(goal_dict)

        if goal_id:
            return {
                "message": "Goal created successfully",
                "goal_id": goal_id,
                "business_id": business_id,
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to create goal")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create goal: {str(e)}")


@app.put("/automation/goals/{goal_id}")
async def update_goal(goal_id: str, update_data: GoalUpdate):
    """Update an existing goal"""
    if not AUTOMATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Automation system not available")

    try:
        # Convert Pydantic model to dict, excluding None values
        update_dict = {
            k: v for k, v in update_data.model_dump().items() if v is not None
        }

        success = db.update_goal(goal_id, update_dict)

        if success:
            return {"message": "Goal updated successfully", "goal_id": goal_id}
        else:
            raise HTTPException(status_code=404, detail="Goal not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update goal: {str(e)}")


@app.delete("/automation/goals/{goal_id}")
async def delete_goal(goal_id: str):
    """Delete a goal"""
    if not AUTOMATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Automation system not available")

    try:
        success = db.delete_goal(goal_id)

        if success:
            return {"message": "Goal deleted successfully", "goal_id": goal_id}
        else:
            raise HTTPException(status_code=404, detail="Goal not found")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete goal: {str(e)}")


@app.post("/automation/business/{business_id}/check-goals")
async def check_business_goals(business_id: str):
    """Check if business goals are being achieved and trigger re-analysis if needed"""
    if not AUTOMATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Automation system not available")

    result = await automation_engine.check_goal_achievement(business_id)
    return result


@app.post("/automation/start")
async def start_automation_scheduler():
    """Start the automation scheduler"""
    if not AUTOMATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Automation system not available")

    try:
        # Start scheduler in background
        asyncio.create_task(automation_engine.run_scheduler())
        return {"message": "Automation scheduler started successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to start scheduler: {str(e)}"
        )


@app.post("/automation/stop")
async def stop_automation_scheduler():
    """Stop the automation scheduler"""
    if not AUTOMATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Automation system not available")

    try:
        automation_engine.stop_scheduler()
        return {"message": "Automation scheduler stopped successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to stop scheduler: {str(e)}"
        )


@app.post("/automation/task/{business_id}/execute")
async def execute_specific_task(business_id: str, task_type: str, agent_type: str):
    """Execute a specific task for a business"""
    if not AUTOMATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Automation system not available")

    try:
        # Find the task
        tasks = automation_engine.get_business_tasks(business_id)
        task_data = next(
            (
                t
                for t in tasks
                if t["task_type"] == task_type and t["agent_type"] == agent_type
            ),
            None,
        )

        if not task_data:
            raise HTTPException(status_code=404, detail="Task not found")

        # Create AutomatedTask object
        from app.api.v0.task_automation import AutomatedTask, TaskFrequency

        task = AutomatedTask(
            business_id=task_data["business_id"],
            business_name=task_data["business_name"],
            agent_type=task_data["agent_type"],
            task_type=task_data["task_type"],
            frequency=TaskFrequency(task_data["frequency"]),
            parameters=task_data.get("parameters", {}),
            task_id=task_data["_id"],
        )

        await automation_engine.execute_task(task)
        return {"message": f"Task {task_type} executed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to execute task: {str(e)}")


@app.get("/automation/tasks")
async def get_all_tasks(status: Optional[str] = None):
    """Get all tasks, optionally filtered by status"""
    if not AUTOMATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Automation system not available")

    try:
        tasks = db.get_all_tasks(status)
        return {"tasks": tasks, "total_count": len(tasks), "status_filter": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get tasks: {str(e)}")


@app.get("/automation/goals")
async def get_all_goals():
    """Get all goals"""
    if not AUTOMATION_AVAILABLE:
        raise HTTPException(status_code=503, detail="Automation system not available")

    try:
        # This would need to be implemented in the database module
        # For now, we'll get goals for all businesses
        all_goals = []
        businesses = db.get_all_businesses()

        for business in businesses:
            goals = automation_engine.get_business_goals(business["_id"])
            all_goals.extend(goals)

        return {"goals": all_goals, "total_count": len(all_goals)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get goals: {str(e)}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5099)
