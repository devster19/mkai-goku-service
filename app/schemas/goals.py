"""
Goal-related Pydantic schemas
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class GoalCreate(BaseModel):
    """Goal creation model"""
    goal_type: str
    target_value: float
    current_value: Optional[float] = 0
    deadline: str
    status: Optional[str] = "on_track"


class GoalUpdate(BaseModel):
    """Goal update model"""
    current_value: Optional[float] = None
    status: Optional[str] = None
    target_value: Optional[float] = None
    deadline: Optional[str] = None


class GoalResponse(BaseModel):
    """Goal response model"""
    goal_id: str
    business_id: str
    goal_type: str
    target_value: float
    current_value: float
    deadline: str
    status: str
    last_updated: str
    created_at: str


class GoalListResponse(BaseModel):
    """Response model for goal listing"""
    goals: List[GoalResponse]
    total_count: int 