"""
Main FastAPI application
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.core.database import db
from app.services.agent_service import agent_service
from app.api.v1 import business, agents

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
    description="A multi-agent system for business analysis and planning - v1 API",
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

# Include V1 API routers only
app.include_router(agents.router, prefix="/api/v1/agents", tags=["agents"])
app.include_router(business.router, prefix="/api/v1", tags=["business"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Multi-Agent Business Analysis System v1",
        "version": settings.VERSION,
        "api_version": "v1",
        "endpoints": {
            "agents": "/api/v1/agents - Agent management and MCP tasks",
            "business": "/api/v1/business - Business analysis workflows"
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
            "api_version": "v1"
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Health check failed: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=5099,
        reload=True
    ) 