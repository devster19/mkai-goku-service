"""
Business service for handling business analysis operations
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import httpx
import asyncio
import json
import logging

from app.core.database import db
from app.schemas.business import BusinessInput, BusinessAnalysisResponse
from app.core.config import settings

logger = logging.getLogger(__name__)


class BusinessService:
    """Service for business analysis operations"""

    def __init__(self):
        self.agent_config = {
            "strategic": {"url": "http://localhost:5001", "port": 5001},
            "creative": {"url": "http://localhost:5002", "port": 5002},
            "financial": {"url": "http://localhost:5003", "port": 5003},
            "sales": {"url": "http://localhost:5004", "port": 5004},
            "manager": {"url": "http://localhost:5005", "port": 5005},
            "analytics": {"url": "http://localhost:5006", "port": 5006},
            "swot": {"url": "http://localhost:5007", "port": 5007},
            "business_model": {"url": "http://localhost:5008", "port": 5008},
        }

    async def process_business_analysis(self, business_data: BusinessInput) -> BusinessAnalysisResponse:
        """Process business analysis using multiple agents"""
        try:
            # Step 1: Send to Strategic Agent
            strategic_response = await self._send_to_agent("strategic", business_data.model_dump())

            # Step 2: Send to SWOT Agent (can run in parallel with other agents)
            swot_response = await self._send_to_agent("swot", business_data.model_dump())

            # Step 3: Send to Business Model Canvas Agent
            bmc_response = await self._send_to_agent("business_model", business_data.model_dump())

            # Step 4: Send to Creative Agent
            creative_response = await self._send_to_agent("creative", business_data.model_dump())

            # Step 5: Send to Financial Agent
            financial_response = await self._send_to_agent("financial", business_data.model_dump())

            # Step 6: Send to Sales Agent
            sales_response = await self._send_to_agent("sales", business_data.model_dump())

            # Step 7: Send to Analytics Agent
            analytics_response = await self._send_to_agent("analytics", business_data.model_dump())

            # Step 8: Send to Manager Agent
            manager_response = await self._send_to_agent("manager", business_data.model_dump())

            # Generate overall recommendations
            overall_recommendations = self._generate_overall_recommendations(
                strategic_response, creative_response, financial_response, 
                sales_response, swot_response, bmc_response, analytics_response
            )

            # Save to database
            business_id = self._save_business_data(business_data, {
                "strategic_plan": strategic_response.get("strategic_plan", {}),
                "creative_analysis": creative_response.get("creative_analysis", {}),
                "financial_analysis": financial_response.get("financial_analysis", {}),
                "sales_strategy": sales_response.get("sales_strategy", {}),
                "swot_analysis": swot_response.get("swot_analysis", {}),
                "business_model_canvas": bmc_response.get("business_model_canvas", {}),
                "analytics_summary": analytics_response.get("analytics_summary", {}),
                "management_summary": manager_response.get("management_summary", {}),
                "overall_recommendations": overall_recommendations
            })

            return BusinessAnalysisResponse(
                business_name=business_data.business_name,
                timestamp=datetime.now().isoformat(),
                business_id=business_id,
                strategic_plan=strategic_response.get("strategic_plan", {}),
                creative_analysis=creative_response.get("creative_analysis", {}),
                financial_analysis=financial_response.get("financial_analysis", {}),
                sales_strategy=sales_response.get("sales_strategy", {}),
                swot_analysis=swot_response.get("swot_analysis", {}),
                business_model_canvas=bmc_response.get("business_model_canvas", {}),
                analytics_summary=analytics_response.get("analytics_summary", {}),
                overall_recommendations=overall_recommendations
            )

        except Exception as e:
            logger.error(f"Error processing business analysis: {e}")
            raise

    async def _send_to_agent(self, agent_type: str, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send business data to a specific agent"""
        try:
            agent_url = self.agent_config[agent_type]["url"]
            message = {
                "agent_type": agent_type,
                "business_data": business_data,
                "timestamp": datetime.now().isoformat(),
                "request_id": f"req_{datetime.now().timestamp()}",
            }

            async with httpx.AsyncClient(timeout=settings.DEFAULT_AGENT_TIMEOUT) as client:
                response = await client.post(
                    f"{agent_url}/receive_message",
                    json=message,
                    headers={"Content-Type": "application/json"},
                )
                response.raise_for_status()
                return response.json()

        except Exception as e:
            logger.error(f"Error communicating with {agent_type} agent: {e}")
            return {}

    def _generate_overall_recommendations(self, strategic, creative, financial, sales, swot, bmc, analytics) -> List[str]:
        """Generate overall recommendations based on all agent responses"""
        recommendations = []
        
        # Add recommendations from each agent
        if strategic and "recommendations" in strategic:
            recommendations.extend(strategic["recommendations"])
        
        if creative and "recommendations" in creative:
            recommendations.extend(creative["recommendations"])
        
        if financial and "recommendations" in financial:
            recommendations.extend(financial["recommendations"])
        
        if sales and "recommendations" in sales:
            recommendations.extend(sales["recommendations"])
        
        if swot and "recommendations" in swot:
            recommendations.extend(swot["recommendations"])
        
        if bmc and "recommendations" in bmc:
            recommendations.extend(bmc["recommendations"])
        
        if analytics and "recommendations" in analytics:
            recommendations.extend(analytics["recommendations"])
        
        # Remove duplicates and limit to top recommendations
        unique_recommendations = list(set(recommendations))
        return unique_recommendations[:10]  # Return top 10 recommendations

    def _save_business_data(self, business_data: BusinessInput, analysis_results: Dict[str, Any]) -> Optional[str]:
        """Save business data and analysis results to database"""
        try:
            collection = db.get_collection("businesses")
            if not collection:
                return None

            # Prepare business document
            business_doc = {
                "business_name": business_data.business_name,
                "business_type": business_data.business_type,
                "location": business_data.location,
                "description": business_data.description,
                "target_market": business_data.target_market,
                "competitors": business_data.competitors,
                "growth_goals": business_data.growth_goals,
                "initial_investment": business_data.initial_investment,
                "team_size": business_data.team_size,
                "unique_value_proposition": business_data.unique_value_proposition,
                "business_model": business_data.business_model,
                "industry": business_data.industry,
                "market_size": business_data.market_size,
                "technology_requirements": business_data.technology_requirements,
                "regulatory_requirements": business_data.regulatory_requirements,
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }

            # Insert business document
            business_result = collection.insert_one(business_doc)
            business_id = str(business_result.inserted_id)

            # Save analysis results
            self._save_analysis_results(business_id, business_data, analysis_results)

            logger.info(f"✅ Saved business '{business_data.business_name}' with ID: {business_id}")
            return business_id

        except Exception as e:
            logger.error(f"❌ Error saving business data: {e}")
            return None

    def _save_analysis_results(self, business_id: str, business_data: BusinessInput, analysis_results: Dict[str, Any]):
        """Save analysis results to database"""
        try:
            collection = db.get_collection("analyses")
            if not collection:
                return

            analysis_doc = {
                "business_id": business_id,
                "business_name": business_data.business_name,
                "business_type": business_data.business_type,
                "strategic_plan": analysis_results.get("strategic_plan", {}),
                "swot_analysis": analysis_results.get("swot_analysis", {}),
                "business_model_canvas": analysis_results.get("business_model_canvas", {}),
                "creative_analysis": analysis_results.get("creative_analysis", {}),
                "financial_analysis": analysis_results.get("financial_analysis", {}),
                "sales_strategy": analysis_results.get("sales_strategy", {}),
                "analytics_summary": analysis_results.get("analytics_summary", {}),
                "management_summary": analysis_results.get("management_summary", {}),
                "overall_recommendations": analysis_results.get("overall_recommendations", []),
                "success_probability": analysis_results.get("analytics_summary", {}).get("success_probability", {}).get("overall_success_rate", "N/A"),
                "created_at": datetime.utcnow(),
            }

            collection.insert_one(analysis_doc)

        except Exception as e:
            logger.error(f"❌ Error saving analysis results: {e}")

    def get_business(self, business_id: str) -> Optional[Dict[str, Any]]:
        """Get business data by ID"""
        try:
            collection = db.get_collection("businesses")
            if not collection:
                return None

            from bson import ObjectId
            business = collection.find_one({"_id": ObjectId(business_id)})
            return db._convert_object_id(business) if business else None

        except Exception as e:
            logger.error(f"❌ Error retrieving business: {e}")
            return None

    def get_analysis(self, business_id: str) -> Optional[Dict[str, Any]]:
        """Get analysis results by business ID"""
        try:
            collection = db.get_collection("analyses")
            if not collection:
                return None

            analysis = collection.find_one({"business_id": business_id})
            return db._convert_object_id(analysis) if analysis else None

        except Exception as e:
            logger.error(f"❌ Error retrieving analysis: {e}")
            return None

    def get_all_businesses(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all businesses with their latest analysis"""
        try:
            businesses_collection = db.get_collection("businesses")
            analyses_collection = db.get_collection("analyses")
            
            if not businesses_collection or not analyses_collection:
                return []

            # Aggregate to get businesses with their latest analysis
            pipeline = [
                {
                    "$lookup": {
                        "from": "analyses",
                        "localField": "_id",
                        "foreignField": "business_id",
                        "as": "analysis"
                    }
                },
                {"$unwind": {"path": "$analysis", "preserveNullAndEmptyArrays": True}},
                {"$sort": {"analysis.created_at": -1}},
                {"$group": {
                    "_id": "$_id",
                    "business": {"$first": "$$ROOT"},
                    "latest_analysis": {"$first": "$analysis"}
                }},
                {"$replaceRoot": {
                    "newRoot": {
                        "$mergeObjects": [
                            "$business",
                            {"analysis": "$latest_analysis"}
                        ]
                    }
                }},
                {"$limit": limit}
            ]

            results = list(businesses_collection.aggregate(pipeline))
            return db._convert_documents(results)

        except Exception as e:
            logger.error(f"❌ Error retrieving businesses: {e}")
            return []

    def search_businesses(self, query: str, business_type: str = None) -> List[Dict[str, Any]]:
        """Search businesses by name or description"""
        try:
            collection = db.get_collection("businesses")
            if not collection:
                return []

            search_query = {
                "$or": [
                    {"business_name": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}},
                    {"target_market": {"$regex": query, "$options": "i"}},
                ]
            }

            if business_type:
                search_query["business_type"] = business_type

            businesses = list(collection.find(search_query))
            return db._convert_documents(businesses)

        except Exception as e:
            logger.error(f"❌ Error searching businesses: {e}")
            return []

    def delete_business(self, business_id: str) -> bool:
        """Delete a business and its associated data"""
        try:
            businesses_collection = db.get_collection("businesses")
            analyses_collection = db.get_collection("analyses")
            
            if not businesses_collection or not analyses_collection:
                return False

            from bson import ObjectId

            # Delete business
            business_result = businesses_collection.delete_one({"_id": ObjectId(business_id)})
            
            # Delete associated analysis
            analyses_collection.delete_many({"business_id": business_id})

            success = business_result.deleted_count > 0
            if success:
                logger.info(f"✅ Deleted business: {business_id}")
            return success

        except Exception as e:
            logger.error(f"❌ Error deleting business: {e}")
            return False


# Global service instance
business_service = BusinessService() 