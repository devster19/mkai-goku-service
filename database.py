"""
MongoDB database operations for business analysis system
"""

import os
import json
from datetime import datetime
from typing import Dict, Any, Optional, List
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BusinessDatabase:
    """MongoDB database operations for business analysis"""

    def __init__(self):
        self.mongodb_uri = os.getenv("MONGODB_URI")
        if not self.mongodb_uri:
            raise ValueError("MONGODB_URI environment variable is required")

        self.client = None
        self.db = None
        self.businesses_collection = None
        self.analyses_collection = None

    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(self.mongodb_uri, serverSelectionTimeoutMS=5000)
            # Test the connection
            self.client.admin.command("ping")
            logger.info("✅ Successfully connected to MongoDB")

            # Get database and collections
            self.db = self.client.business_analysis
            self.businesses_collection = self.db.businesses
            self.analyses_collection = self.db.analyses

            # Create indexes for better performance
            self.businesses_collection.create_index("business_name")
            self.businesses_collection.create_index("business_type")
            self.businesses_collection.create_index("created_at")
            self.analyses_collection.create_index("business_id")
            self.analyses_collection.create_index("created_at")

            return True

        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            logger.error(f"❌ Failed to connect to MongoDB: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Database connection error: {e}")
            return False

    def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            logger.info("🔌 Disconnected from MongoDB")

    def save_business(
        self, business_data: Dict[str, Any], analysis_results: Dict[str, Any]
    ) -> Optional[str]:
        """Save business data and analysis results to MongoDB"""
        try:
            if not self.client:
                if not self.connect():
                    return None

            # Prepare business document
            business_doc = {
                "business_name": business_data.get("business_name"),
                "business_type": business_data.get("business_type"),
                "location": business_data.get("location"),
                "description": business_data.get("description"),
                "target_market": business_data.get("target_market"),
                "competitors": business_data.get("competitors", []),
                "growth_goals": business_data.get("growth_goals", []),
                "initial_investment": business_data.get("initial_investment"),
                "team_size": business_data.get("team_size"),
                "unique_value_proposition": business_data.get(
                    "unique_value_proposition"
                ),
                "business_model": business_data.get("business_model"),
                "industry": business_data.get("industry"),
                "market_size": business_data.get("market_size"),
                "technology_requirements": business_data.get(
                    "technology_requirements", []
                ),
                "regulatory_requirements": business_data.get(
                    "regulatory_requirements", []
                ),
                "created_at": datetime.utcnow(),
                "updated_at": datetime.utcnow(),
            }

            # Insert business document
            business_result = self.businesses_collection.insert_one(business_doc)
            business_id = str(business_result.inserted_id)

            # Prepare analysis document
            analysis_doc = {
                "business_id": business_id,
                "business_name": business_data.get("business_name"),
                "business_type": business_data.get("business_type"),
                "strategic_plan": analysis_results.get("strategic_plan", {}),
                "swot_analysis": analysis_results.get("swot_analysis", {}),
                "business_model_canvas": analysis_results.get(
                    "business_model_canvas", {}
                ),
                "creative_analysis": analysis_results.get("creative_analysis", {}),
                "financial_analysis": analysis_results.get("financial_analysis", {}),
                "sales_strategy": analysis_results.get("sales_strategy", {}),
                "analytics_summary": analysis_results.get("analytics_summary", {}),
                "management_summary": analysis_results.get("management_summary", {}),
                "overall_recommendations": analysis_results.get(
                    "overall_recommendations", []
                ),
                "success_probability": analysis_results.get("analytics_summary", {})
                .get("success_probability", {})
                .get("overall_success_rate", "N/A"),
                "created_at": datetime.utcnow(),
            }

            # Insert analysis document
            self.analyses_collection.insert_one(analysis_doc)

            logger.info(
                f"✅ Saved business '{business_data.get('business_name')}' with ID: {business_id}"
            )
            return business_id

        except Exception as e:
            logger.error(f"❌ Error saving business data: {e}")
            return None

    def get_business(self, business_id: str) -> Optional[Dict[str, Any]]:
        """Get business data by ID"""
        try:
            if not self.client:
                if not self.connect():
                    return None

            from bson import ObjectId

            business = self.businesses_collection.find_one(
                {"_id": ObjectId(business_id)}
            )
            if business:
                business["_id"] = str(business["_id"])
                return business
            return None

        except Exception as e:
            logger.error(f"❌ Error retrieving business: {e}")
            return None

    def get_analysis(self, business_id: str) -> Optional[Dict[str, Any]]:
        """Get analysis results by business ID"""
        try:
            if not self.client:
                if not self.connect():
                    return None

            from bson import ObjectId

            analysis = self.analyses_collection.find_one({"business_id": business_id})
            if analysis:
                analysis["_id"] = str(analysis["_id"])
                return analysis
            return None

        except Exception as e:
            logger.error(f"❌ Error retrieving analysis: {e}")
            return None

    def get_all_businesses(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get all businesses with their latest analysis"""
        try:
            if not self.client:
                if not self.connect():
                    return []

            # Aggregate to get businesses with their latest analysis
            pipeline = [
                {
                    "$lookup": {
                        "from": "analyses",
                        "localField": "_id",
                        "foreignField": "business_id",
                        "as": "analysis",
                    }
                },
                {"$unwind": {"path": "$analysis", "preserveNullAndEmptyArrays": True}},
                {"$sort": {"created_at": -1}},
                {"$limit": limit},
            ]

            businesses = list(self.businesses_collection.aggregate(pipeline))

            # Convert ObjectId to string
            for business in businesses:
                business["_id"] = str(business["_id"])
                if business.get("analysis"):
                    business["analysis"]["_id"] = str(business["analysis"]["_id"])

            return businesses

        except Exception as e:
            logger.error(f"❌ Error retrieving businesses: {e}")
            return []

    def search_businesses(
        self, query: str, business_type: str = None
    ) -> List[Dict[str, Any]]:
        """Search businesses by name or description"""
        try:
            if not self.client:
                if not self.connect():
                    return []

            # Build search filter
            search_filter = {
                "$or": [
                    {"business_name": {"$regex": query, "$options": "i"}},
                    {"description": {"$regex": query, "$options": "i"}},
                    {"industry": {"$regex": query, "$options": "i"}},
                ]
            }

            if business_type:
                search_filter["business_type"] = business_type

            businesses = list(
                self.businesses_collection.find(search_filter)
                .sort("created_at", -1)
                .limit(20)
            )

            # Convert ObjectId to string
            for business in businesses:
                business["_id"] = str(business["_id"])

            return businesses

        except Exception as e:
            logger.error(f"❌ Error searching businesses: {e}")
            return []

    def delete_business(self, business_id: str) -> bool:
        """Delete business and its analysis"""
        try:
            if not self.client:
                if not self.connect():
                    return False

            from bson import ObjectId

            obj_id = ObjectId(business_id)

            # Delete analysis first
            self.analyses_collection.delete_many({"business_id": business_id})

            # Delete business
            result = self.businesses_collection.delete_one({"_id": obj_id})

            return result.deleted_count > 0

        except Exception as e:
            logger.error(f"❌ Error deleting business: {e}")
            return False


# Global database instance
db = BusinessDatabase()
