"""
Business API routes
"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from app.schemas.business import (
    BusinessInput,
    BusinessAnalysisResponse,
    BusinessResponse,
    MinimalBusinessInput,
)
from app.services.business_service import business_service

router = APIRouter(prefix="/business", tags=["business"])


@router.post("/create", response_model=BusinessResponse)
async def create_business(business_data: MinimalBusinessInput):
    """Create a new business with only essential fields"""
    try:
        # Convert minimal input to full BusinessInput
        full_business_data = BusinessInput(
            business_name=business_data.business_name,
            description=business_data.description,
            business_type=business_data.business_type,
            location=business_data.location,
            target_market=business_data.target_market,
            competitors=business_data.competitors,
            growth_goals=business_data.growth_goals,
        )

        # Create business using the service
        business_id = business_service.create_business(full_business_data)
        if not business_id:
            raise HTTPException(
                status_code=500, detail="Failed to create business - no ID returned"
            )

        # Return the created business
        business = business_service.get_business(business_id)
        if not business:
            raise HTTPException(
                status_code=500, detail="Business created but could not retrieve it"
            )

        return business
    except HTTPException:
        raise
    except Exception as e:
        import traceback

        error_detail = (
            f"Failed to create business: {str(e)}\nTraceback: {traceback.format_exc()}"
        )
        raise HTTPException(status_code=500, detail=error_detail)


@router.post("/process", response_model=BusinessAnalysisResponse)
async def process_business(business_input: BusinessInput):
    """Process business analysis using multiple agents"""
    try:
        return await business_service.process_business_analysis(business_input)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to process business: {str(e)}"
        )


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
        raise HTTPException(
            status_code=500, detail=f"Failed to get businesses: {str(e)}"
        )


@router.get("/search", response_model=list)
async def search_businesses(
    q: str = Query(..., min_length=2, description="Search query"),
    business_type: Optional[str] = Query(None, description="Filter by business type"),
):
    """Search businesses by name, description, or target market"""
    try:
        businesses = business_service.search_businesses(q, business_type)
        return businesses
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to search businesses: {str(e)}"
        )


@router.delete("/{business_id}")
async def delete_business(business_id: str):
    """Delete a business and its associated data"""
    try:
        success = business_service.delete_business(business_id)
        if success:
            return {
                "message": "Business deleted successfully",
                "business_id": business_id,
            }
        else:
            raise HTTPException(status_code=404, detail="Business not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete business: {str(e)}"
        )
