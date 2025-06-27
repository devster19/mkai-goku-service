"""
Business-related Pydantic schemas
"""
from pydantic import BaseModel
from typing import List, Dict, Any, Optional


class BusinessInput(BaseModel):
    """Business input model for analysis requests"""
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
    business_model: Optional[str] = None  # e.g., "b2c", "b2b", "marketplace", "subscription"
    industry: Optional[str] = None  # e.g., "food_beverage", "technology", "retail", "services"
    market_size: Optional[str] = None  # e.g., "local", "regional", "national", "international"
    technology_requirements: Optional[List[str]] = None
    regulatory_requirements: Optional[List[str]] = None


class BusinessAnalysisResponse(BaseModel):
    """Business analysis response model"""
    business_name: str
    timestamp: str
    business_id: Optional[str] = None
    strategic_plan: Dict[str, Any]
    creative_analysis: Dict[str, Any]
    financial_analysis: Dict[str, Any]
    sales_strategy: Dict[str, Any]
    swot_analysis: Dict[str, Any]
    business_model_canvas: Dict[str, Any]
    analytics_summary: Dict[str, Any]
    overall_recommendations: List[str]


class BusinessResponse(BaseModel):
    """Business data response model"""
    business_id: str
    business_name: str
    business_type: str
    location: str
    description: str
    target_market: str
    competitors: List[str]
    growth_goals: List[str]
    initial_investment: Optional[float] = None
    team_size: Optional[int] = None
    unique_value_proposition: Optional[str] = None
    business_model: Optional[str] = None
    industry: Optional[str] = None
    market_size: Optional[str] = None
    technology_requirements: Optional[List[str]] = None
    regulatory_requirements: Optional[List[str]] = None
    created_at: str
    updated_at: str 