"""
Main FastAPI application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from mangum import Mangum

from app.core.config import settings
from app.core.database import db
from app.services.agent_service import agent_service
from app.api.v1 import business, agents

# Import v0 API for automation endpoints
try:
    from app.api.v0 import main as v0_main
    V0_AVAILABLE = True
except ImportError:
    V0_AVAILABLE = False
    print("⚠️ V0 API not available. Automation endpoints will not be available.")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("🚀 Starting Multi-Agent Business Analysis System v1...")
    
    # Connect to database
    try:
        if db.connect():
            logger.info("✅ Database connected successfully")
        else:
            logger.error("❌ Failed to connect to database")
    except Exception as e:
        logger.error(f"❌ Database connection error: {e}")
    
    # Initialize default agent types
    try:
        success = agent_service.initialize_default_agent_types()
        if success:
            logger.info("✅ Default agent types initialized")
        else:
            logger.warning("⚠️ Agent types initialization failed or already exists")
    except Exception as e:
        logger.error(f"❌ Error initializing agent types: {e}")
    
    yield
    
    # Shutdown
    logger.info("🛑 Shutting down...")
    try:
        db.disconnect()
        logger.info("✅ Application shutdown complete")
    except Exception as e:
        logger.error(f"❌ Error closing database connection: {e}")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="A multi-agent system for business analysis and planning - v1 API with v0 automation",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include V1 API routers
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(business.router, prefix="/api/v1", tags=["business"])

# Include V0 API for automation endpoints
if V0_AVAILABLE:
    # Add v0 automation endpoints directly
    from app.api.v0.main import (
        get_automation_summary,
        get_business_tasks,
        create_business_task,
        update_task,
        delete_task,
        get_business_goals,
        create_business_goal,
        update_goal,
        delete_goal,
        check_business_goals,
        start_automation_scheduler,
        stop_automation_scheduler,
        execute_specific_task,
        get_all_tasks,
        get_all_goals
    )
    
    # Add automation endpoints to the main app
    app.add_api_route("/automation/summary", get_automation_summary, methods=["GET"], tags=["automation"])
    app.add_api_route("/automation/business/{business_id}/tasks", get_business_tasks, methods=["GET"], tags=["automation"])
    app.add_api_route("/automation/business/{business_id}/tasks", create_business_task, methods=["POST"], tags=["automation"])
    app.add_api_route("/automation/tasks/{task_id}", update_task, methods=["PUT"], tags=["automation"])
    app.add_api_route("/automation/tasks/{task_id}", delete_task, methods=["DELETE"], tags=["automation"])
    app.add_api_route("/automation/business/{business_id}/goals", get_business_goals, methods=["GET"], tags=["automation"])
    app.add_api_route("/automation/business/{business_id}/goals", create_business_goal, methods=["POST"], tags=["automation"])
    app.add_api_route("/automation/goals/{goal_id}", update_goal, methods=["PUT"], tags=["automation"])
    app.add_api_route("/automation/goals/{goal_id}", delete_goal, methods=["DELETE"], tags=["automation"])
    app.add_api_route("/automation/business/{business_id}/check-goals", check_business_goals, methods=["POST"], tags=["automation"])
    app.add_api_route("/automation/start", start_automation_scheduler, methods=["POST"], tags=["automation"])
    app.add_api_route("/automation/stop", stop_automation_scheduler, methods=["POST"], tags=["automation"])
    app.add_api_route("/automation/task/{business_id}/execute", execute_specific_task, methods=["POST"], tags=["automation"])
    app.add_api_route("/automation/tasks", get_all_tasks, methods=["GET"], tags=["automation"])
    app.add_api_route("/automation/goals", get_all_goals, methods=["GET"], tags=["automation"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Multi-Agent Business Analysis System v1",
        "version": settings.VERSION,
        "api_version": "v1",
        "endpoints": {
            "agents": "/api/v1/agents - Agent management and MCP tasks",
            "business": "/api/v1/business - Business analysis workflows",
            "automation": "/automation/* - Business automation (v0 API)"
        },
        "docs": "/docs",
        "redoc": "/redoc"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        # Check database connection
        if not db.client:
            raise HTTPException(status_code=503, detail="Database not connected")
        
        return {
            "status": "healthy",
            "database": "connected",
            "version": settings.VERSION,
            "api_version": "v1",
            "automation_available": V0_AVAILABLE
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")


handler = Mangum(app)


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=5099,
        reload=True
    ) 