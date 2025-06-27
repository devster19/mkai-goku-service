"""
Business API routes
"""
from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.schemas.business import BusinessInput, BusinessAnalysisResponse, BusinessResponse
from app.services.business_service import business_service

router = APIRouter(prefix="/business", tags=["business"])


@router.post("/process", response_model=BusinessAnalysisResponse)
async def process_business(business_input: BusinessInput):
    """Process business analysis using multiple agents"""
    try:
        return await business_service.process_business_analysis(business_input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process business: {str(e)}")


@router.get("/{business_id}", response_model=BusinessResponse)
async def get_business(business_id: str):
    """Get business data by ID"""
    business = business_service.get_business(business_id)
    if not business:
        raise HTTPException(status_code=404, detail="Business not found")
    return business


@router.get("/{business_id}/analysis", response_model=dict)
async def get_analysis(business_id: str):
    """Get analysis results by business ID"""
    analysis = business_service.get_analysis(business_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis


@router.get("/", response_model=list)
async def get_all_businesses(limit: int = Query(50, ge=1, le=100)):
    """Get all businesses with their latest analysis"""
    try:
        businesses = business_service.get_all_businesses(limit)
        return businesses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get businesses: {str(e)}")


@router.get("/search", response_model=list)
async def search_businesses(
    q: str = Query(..., min_length=2, description="Search query"),
    business_type: Optional[str] = Query(None, description="Filter by business type")
):
    """Search businesses by name, description, or target market"""
    try:
        businesses = business_service.search_businesses(q, business_type)
        return businesses
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search businesses: {str(e)}")


@router.delete("/{business_id}")
async def delete_business(business_id: str):
    """Delete a business and its associated data"""
    try:
        success = business_service.delete_business(business_id)
        if success:
            return {"message": "Business deleted successfully", "business_id": business_id}
        else:
            raise HTTPException(status_code=404, detail="Business not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete business: {str(e)}") 