"""
Business service for handling business analysis operations
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
import asyncio
import json
import logging

from app.core.database import db
from app.schemas.business import BusinessInput, BusinessAnalysisResponse
from app.core.config import settings

# Import agent utilities
try:
    from app.utils.agents import (
        analyze_strategic,
        analyze_swot,
        analyze_business_model,
        analyze_creative,
        analyze_financial,
        analyze_sales,
        analyze_analytics,
        analyze_manager,
        assign_tasks_to_agents,
    )
    AGENTS_AVAILABLE = True
    print("✅ Agent utilities loaded successfully")
except ImportError as e:
    AGENTS_AVAILABLE = False
    print(f"⚠️ Agent utilities not available: {e}")

# Import automation engine if available
try:
    from app.api.v0.task_automation import automation_engine
    AUTOMATION_AVAILABLE = True
except ImportError:
    AUTOMATION_AVAILABLE = False
    print("⚠️ Task automation module not available. Automated tasks will not be created.")

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

    async def process_business_analysis(
        self, business_data: BusinessInput
    ) -> BusinessAnalysisResponse:
        """Process business analysis using multiple agents with v0 orchestration logic"""
        try:
            if not AGENTS_AVAILABLE:
                # Fallback to basic analysis without agents
                return await self._process_basic_analysis(business_data)

            # Step 1: Send to Strategic Agent first
            print("🔍 Starting strategic analysis...")
            strategic_response = await analyze_strategic(business_data.model_dump())
            strategic_plan = strategic_response.get("strategic_plan", {})

            # Step 2: Send to SWOT Agent with strategic plan data
            print("🔍 Starting SWOT analysis...")
            swot_response = await analyze_swot(business_data.model_dump(), strategic_plan)
            swot_analysis = swot_response.get("swot_analysis", {})

            # Step 3: Send to Business Model Canvas agent with strategic plan and SWOT data
            print("🔍 Starting Business Model Canvas analysis...")
            bmc_response = await analyze_business_model(
                business_data.model_dump(), strategic_plan, swot_analysis
            )
            bmc_analysis = bmc_response.get("business_model_canvas", {})

            # Step 4: Send to Creative, Financial, and Sales agents in parallel with strategic plan data
            print("🔍 Starting parallel analysis (Creative, Financial, Sales)...")
            creative_task = analyze_creative(business_data.model_dump(), strategic_plan)
            financial_task = analyze_financial(business_data.model_dump(), strategic_plan)
            sales_task = analyze_sales(business_data.model_dump(), strategic_plan)

            # Wait for all parallel tasks to complete
            creative_response, financial_response, sales_response = await asyncio.gather(
                creative_task, financial_task, sales_task
            )

            creative_analysis = creative_response.get("creative_analysis", {})
            financial_analysis = financial_response.get("financial_analysis", {})
            sales_strategy = sales_response.get("sales_strategy", {})

            # Step 5: Send to Analytics agent with all the data from previous agents
            print("🔍 Starting analytics analysis...")
            all_agent_data = {
                "strategic_plan": strategic_plan,
                "creative_analysis": creative_analysis,
                "financial_analysis": financial_analysis,
                "sales_strategy": sales_strategy,
                "swot_analysis": swot_analysis,
                "business_model_canvas": bmc_analysis,
            }
            analytics_response = await analyze_analytics(business_data.model_dump(), all_agent_data)
            analytics_summary = analytics_response.get("analytics_summary", {})

            # Step 6: Send to Manager agent separately
            print("🔍 Starting management analysis...")
            manager_response = await analyze_manager(business_data.model_dump(), all_agent_data)
            management_summary = manager_response.get("management_summary", {})
            dynamic_task_assignments = manager_response.get("dynamic_task_assignments", {})

            # Step 7: Generate overall recommendations
            overall_recommendations = self._generate_overall_recommendations(
                strategic_plan, creative_analysis, financial_analysis, sales_strategy, 
                swot_analysis, bmc_analysis, analytics_summary
            )

            # Step 8: Assign tasks to agents using AI
            print("🔍 Assigning tasks to agents...")
            task_assignments = await assign_tasks_to_agents(business_data.model_dump(), all_agent_data)

            # Step 9: Save to database
            business_id = self.save_business_data(
                business_data,
                {
                    "strategic_plan": strategic_plan,
                    "creative_analysis": creative_analysis,
                    "financial_analysis": financial_analysis,
                    "sales_strategy": sales_strategy,
                    "swot_analysis": swot_analysis,
                    "business_model_canvas": bmc_analysis,
                    "analytics_summary": analytics_summary,
                    "management_summary": management_summary,
                    "task_assignments": task_assignments,
                    "dynamic_task_assignments": dynamic_task_assignments,
                },
            )

            # Step 10: Create automation if available
            if AUTOMATION_AVAILABLE:
                try:
                    print("🔍 Creating business automation...")
                    automation_engine.create_business_automation(
                        business_id, business_data.model_dump()
                    )
                    print("✅ Business automation created successfully")
                except Exception as e:
                    print(f"⚠️ Failed to create business automation: {e}")

            return BusinessAnalysisResponse(
                business_id=business_id,
                business_name=business_data.business_name,
                analysis_completed=True,
                strategic_plan=strategic_plan,
                creative_analysis=creative_analysis,
                financial_analysis=financial_analysis,
                sales_strategy=sales_strategy,
                swot_analysis=swot_analysis,
                business_model_canvas=bmc_analysis,
                analytics_summary=analytics_summary,
                management_summary=management_summary,
                overall_recommendations=overall_recommendations,
                task_assignments=task_assignments,
                dynamic_task_assignments=dynamic_task_assignments,
                created_at=datetime.now().isoformat(),
            )

        except Exception as e:
            logger.error(f"Error in process_business_analysis: {e}")
            raise e

    async def _send_to_agent_with_message(
        self, agent_type: str, message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send message to a specific agent with custom message structure"""
        try:
            agent_url = self.agent_config[agent_type]["url"]

            async with httpx.AsyncClient(
                timeout=settings.DEFAULT_AGENT_TIMEOUT
            ) as client:
                response = await client.post(
                    f"{agent_url}/receive_message",
                    json=message,
                    headers={"Content-Type": "application/json"},
                )
                response.raise_for_status()
                return response.json()

        except Exception as e:
            logger.error(f"Error communicating with {agent_type} agent: {e}")
            # Return fallback response when agent is not available
            return self._get_fallback_response(agent_type, message.get("business_data", {}))

    def _get_fallback_response(self, agent_type: str, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback response when agent is not available"""
        business_name = business_data.get("business_name", "Unknown Business")
        
        fallback_responses = {
            "strategic": {
                "strategic_plan": {
                    "business_name": business_name,
                    "vision": f"To become a leading {business_data.get('business_type', 'business')} in the market",
                    "mission": f"To provide exceptional value to our customers",
                    "goals": ["Increase market share", "Improve customer satisfaction", "Expand operations"],
                    "strategies": ["Market penetration", "Product development", "Strategic partnerships"]
                }
            },
            "swot": {
                "swot_analysis": {
                    "strengths": ["Strong business concept", "Clear target market", "Unique value proposition"],
                    "weaknesses": ["Limited initial resources", "New market entry", "Need for brand recognition"],
                    "opportunities": ["Growing market demand", "Technology advancement", "Market expansion"],
                    "threats": ["Competition", "Market volatility", "Regulatory changes"],
                    "action_plan": {
                        "immediate_actions": [
                            "Leverage strengths to capitalize on opportunities",
                            "Address weaknesses through strategic planning",
                            "Develop contingency plans for identified threats",
                            "Focus on building competitive advantages"
                        ]
                    }
                }
            },
            "business_model": {
                "business_model_canvas": {
                    "key_partners": ["Suppliers", "Technology providers", "Marketing partners"],
                    "key_activities": ["Product development", "Marketing", "Customer service"],
                    "value_propositions": ["Quality products", "Excellent service", "Competitive pricing"],
                    "customer_relationships": ["Personal assistance", "Self-service", "Community"],
                    "customer_segments": [business_data.get("target_market", "General market")],
                    "key_resources": ["Human resources", "Technology", "Brand"],
                    "channels": ["Online", "Direct sales", "Partnerships"],
                    "cost_structure": ["Operational costs", "Marketing", "Technology"],
                    "revenue_streams": ["Product sales", "Service fees", "Subscriptions"],
                }
            },
            "creative": {
                "creative_analysis": {
                    "brand_identity": f"Modern, innovative {business_data.get('business_type', 'business')}",
                    "marketing_ideas": ["Social media campaigns", "Influencer partnerships", "Content marketing"],
                    "unique_angles": ["Customer-centric approach", "Technology integration", "Sustainability focus"],
                }
            },
            "financial": {
                "financial_analysis": {
                    "startup_costs": business_data.get("initial_investment", 50000),
                    "projected_revenue": "To be determined based on market analysis",
                    "break_even_analysis": "6-12 months projected",
                    "funding_recommendations": ["Bootstrap initially", "Seek angel investment", "Consider crowdfunding"],
                }
            },
            "sales": {
                "sales_strategy": {
                    "target_customers": [business_data.get("target_market", "General market")],
                    "sales_channels": ["Direct sales", "Online platform", "Partnerships"],
                    "pricing_strategy": "Competitive pricing with value-based options",
                    "sales_process": ["Lead generation", "Qualification", "Presentation", "Closing"],
                }
            },
            "analytics": {
                "analytics_summary": {
                    "market_size": business_data.get("market_size", "To be analyzed"),
                    "competition_level": "Moderate to high",
                    "success_probability": {"overall_success_rate": "70%"},
                    "key_metrics": ["Customer acquisition cost", "Lifetime value", "Conversion rate"],
                }
            },
            "manager": {
                "management_summary": {
                    "team_structure": f"Team size: {business_data.get('team_size', 'To be determined')}",
                    "operational_plan": ["Phase 1: Setup", "Phase 2: Launch", "Phase 3: Scale"],
                    "risk_management": ["Market research", "Financial planning", "Legal compliance"],
                    "success_factors": ["Strong leadership", "Clear vision", "Customer focus"]
                }
            }
        }
        
        return fallback_responses.get(agent_type, {})

    def _generate_overall_recommendations(
        self, strategic, creative, financial, sales, swot, bmc, analytics
    ) -> List[Dict[str, Any]]:
        """Generate dynamic overall recommendations with timelines and business roadmap"""
        recommendations = []
        
        # Extract business name for context
        business_name = strategic.get("business_name", "Your Business")
        business_type = strategic.get("business_type", "business")
        
        # Week 1-2: Foundation Phase
        recommendations.append({
            "phase": "Foundation (Week 1-2)",
            "priority": "Critical",
            "recommendations": [
                {
                    "task": f"Conduct market research and validation for {business_name}",
                    "timeline": "Week 1",
                    "agent": "strategic_agent",
                    "description": "Analyze market size, competition, and validate business concept",
                    "expected_outcome": "Market validation report with go/no-go decision",
                    "dependencies": [],
                    "success_metrics": ["Market size confirmed", "Competition analyzed", "Target market validated"]
                },
                {
                    "task": f"Create financial projections and budget for {business_name}",
                    "timeline": "Week 1-2",
                    "agent": "financial_agent",
                    "description": "Develop 3-year financial forecast and operational budget",
                    "expected_outcome": "Financial model with cash flow projections",
                    "dependencies": ["Market research"],
                    "success_metrics": ["Budget created", "Cash flow projected", "Funding needs identified"]
                },
                {
                    "task": f"Develop brand identity for {business_name}",
                    "timeline": "Week 2",
                    "agent": "creative_agent",
                    "description": "Design logo, color scheme, and brand guidelines",
                    "expected_outcome": "Complete brand identity package",
                    "dependencies": ["Market research"],
                    "success_metrics": ["Logo designed", "Brand guidelines created", "Visual identity established"]
                }
            ]
        })
        
        # Week 3-4: Strategy Phase
        recommendations.append({
            "phase": "Strategy Development (Week 3-4)",
            "priority": "High",
            "recommendations": [
                {
                    "task": f"Create strategic growth plan for {business_name}",
                    "timeline": "Week 3",
                    "agent": "strategic_agent",
                    "description": "Develop 12-month strategic roadmap with milestones",
                    "expected_outcome": "Strategic plan with KPIs and milestones",
                    "dependencies": ["Market research", "Financial projections"],
                    "success_metrics": ["Strategic plan completed", "KPIs defined", "Milestones set"]
                },
                {
                    "task": f"Develop sales strategy and process for {business_name}",
                    "timeline": "Week 3-4",
                    "agent": "sales_agent",
                    "description": "Create sales funnel and customer acquisition strategy",
                    "expected_outcome": "Sales strategy document and process flow",
                    "dependencies": ["Brand identity", "Strategic plan"],
                    "success_metrics": ["Sales process defined", "Customer acquisition strategy", "Sales funnel created"]
                },
                {
                    "task": f"Set up performance tracking system for {business_name}",
                    "timeline": "Week 4",
                    "agent": "analytics_agent",
                    "description": "Implement KPI tracking and analytics dashboard",
                    "expected_outcome": "Analytics dashboard with key metrics",
                    "dependencies": ["Strategic plan"],
                    "success_metrics": ["Dashboard created", "KPIs tracked", "Reporting system established"]
                }
            ]
        })
        
        # Week 5-8: Launch Preparation
        recommendations.append({
            "phase": "Launch Preparation (Week 5-8)",
            "priority": "High",
            "recommendations": [
                {
                    "task": f"Launch marketing content strategy for {business_name}",
                    "timeline": "Week 5-6",
                    "agent": "creative_agent",
                    "description": "Create content calendar and marketing materials",
                    "expected_outcome": "Content strategy and initial marketing assets",
                    "dependencies": ["Brand identity", "Sales strategy"],
                    "success_metrics": ["Content calendar created", "Marketing materials ready", "Social media presence established"]
                },
                {
                    "task": f"Execute customer acquisition campaign for {business_name}",
                    "timeline": "Week 6-8",
                    "agent": "sales_agent",
                    "description": "Launch marketing campaigns to acquire customers",
                    "expected_outcome": "Customer acquisition pipeline and results",
                    "dependencies": ["Marketing content", "Sales strategy"],
                    "success_metrics": ["Campaign launched", "Leads generated", "Customer pipeline created"]
                },
                {
                    "task": f"Optimize revenue model for {business_name}",
                    "timeline": "Week 7-8",
                    "agent": "business_model_agent",
                    "description": "Review and optimize pricing and revenue streams",
                    "expected_outcome": "Optimized revenue model and pricing strategy",
                    "dependencies": ["Financial projections", "Sales strategy"],
                    "success_metrics": ["Pricing optimized", "Revenue streams defined", "Business model validated"]
                }
            ]
        })
        
        # Month 2-3: Growth Phase
        recommendations.append({
            "phase": "Growth & Optimization (Month 2-3)",
            "priority": "Medium",
            "recommendations": [
                {
                    "task": f"Analyze customer data and market trends for {business_name}",
                    "timeline": "Month 2",
                    "agent": "analytics_agent",
                    "description": "Analyze customer behavior and market insights",
                    "expected_outcome": "Customer insights and market analysis report",
                    "dependencies": ["Performance tracking", "Customer acquisition"],
                    "success_metrics": ["Customer insights gathered", "Market trends analyzed", "Optimization opportunities identified"]
                },
                {
                    "task": f"Develop partnership strategy for {business_name}",
                    "timeline": "Month 2-3",
                    "agent": "business_model_agent",
                    "description": "Identify and develop strategic partnerships",
                    "expected_outcome": "Partnership strategy and potential partner list",
                    "dependencies": ["Revenue model", "Market analysis"],
                    "success_metrics": ["Partnerships identified", "Partnership strategy created", "Partnerships initiated"]
                },
                {
                    "task": f"Scale operations for {business_name}",
                    "timeline": "Month 3",
                    "agent": "manager_agent",
                    "description": "Optimize operational processes and scale efficiently",
                    "expected_outcome": "Scaled operations with improved efficiency",
                    "dependencies": ["Customer insights", "Partnership strategy"],
                    "success_metrics": ["Operations scaled", "Efficiency improved", "Growth capacity increased"]
                }
            ]
        })
        
        # Add business-type specific recommendations
        if business_type == "coffee_shop":
            recommendations.append({
                "phase": "Coffee Shop Specific (Week 4-6)",
                "priority": "High",
                "recommendations": [
                    {
                        "task": f"Design coffee shop interior concept for {business_name}",
                        "timeline": "Week 4-5",
                        "agent": "creative_agent",
                        "description": "Create interior design concept and branding materials",
                        "expected_outcome": "Interior design concept and visual mockups",
                        "dependencies": ["Brand identity"],
                        "success_metrics": ["Interior design completed", "Visual mockups created", "Branding materials ready"]
                    },
                    {
                        "task": f"Launch coffee shop grand opening campaign for {business_name}",
                        "timeline": "Week 5-6",
                        "agent": "sales_agent",
                        "description": "Plan and execute grand opening marketing campaign",
                        "expected_outcome": "Grand opening campaign with customer acquisition",
                        "dependencies": ["Interior design", "Marketing content"],
                        "success_metrics": ["Grand opening planned", "Campaign executed", "Customers acquired"]
                    }
                ]
            })
        
        elif business_type == "tech_startup":
            recommendations.append({
                "phase": "Tech Startup Specific (Week 3-6)",
                "priority": "High",
                "recommendations": [
                    {
                        "task": f"Develop fundraising strategy for {business_name}",
                        "timeline": "Week 3-4",
                        "agent": "strategic_agent",
                        "description": "Create pitch deck and fundraising strategy",
                        "expected_outcome": "Pitch deck and investor outreach plan",
                        "dependencies": ["Market research", "Financial projections"],
                        "success_metrics": ["Pitch deck created", "Fundraising strategy", "Investor list prepared"]
                    },
                    {
                        "task": f"Create tech product marketing materials for {business_name}",
                        "timeline": "Week 4-6",
                        "agent": "creative_agent",
                        "description": "Design product website and marketing materials",
                        "expected_outcome": "Product website and marketing assets",
                        "dependencies": ["Brand identity", "Fundraising strategy"],
                        "success_metrics": ["Website created", "Marketing materials ready", "Product positioning defined"]
                    }
                ]
            })
        
        return recommendations

    def create_business(self, business_data: BusinessInput) -> Optional[str]:
        """Create a new business without analysis"""
        try:
            logger.info(f"🔍 Creating business: {business_data.business_name}")
            business_id = self.save_business_data(business_data, {})
            if business_id:
                logger.info(f"✅ Successfully created business with ID: {business_id}")
            else:
                logger.error(
                    f"❌ Failed to create business: {business_data.business_name}"
                )
            return business_id
        except Exception as e:
            logger.error(f"❌ Exception in create_business: {e}")
            return None

    def save_business_data(
        self, business_data: BusinessInput, analysis_results: Dict[str, Any]
    ) -> Optional[str]:
        """Save business data and analysis results to database"""
        try:
            logger.info(f"🔍 Getting businesses collection...")
            collection = db.get_collection("businesses")
            if collection is None:
                logger.error(f"❌ Could not get businesses collection")
                return None

            logger.info(f"🔍 Preparing business document...")
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

            logger.info(f"🔍 Inserting business document...")
            # Insert business document
            business_result = collection.insert_one(business_doc)
            business_id = str(business_result.inserted_id)

            # Save analysis results if any
            if analysis_results:
                self._save_analysis_results(
                    business_id, business_data, analysis_results
                )

            logger.info(
                f"✅ Saved business '{business_data.business_name}' with ID: {business_id}"
            )
            return business_id

        except Exception as e:
            logger.error(f"❌ Error saving business data: {e}")
            import traceback

            logger.error(f"❌ Traceback: {traceback.format_exc()}")
            return None

    def _save_analysis_results(
        self,
        business_id: str,
        business_data: BusinessInput,
        analysis_results: Dict[str, Any],
    ):
        """Save analysis results to database"""
        try:
            collection = db.get_collection("analyses")
            if collection is None:
                return

            analysis_doc = {
                "business_id": business_id,
                "business_name": business_data.business_name,
                "business_type": business_data.business_type,
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

            collection.insert_one(analysis_doc)

        except Exception as e:
            logger.error(f"❌ Error saving analysis results: {e}")

    def get_business(self, business_id: str) -> Optional[Dict[str, Any]]:
        """Get business data by ID"""
        try:
            collection = db.get_collection("businesses")
            if collection is None:
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
            if collection is None:
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

            if businesses_collection is None or analyses_collection is None:
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
                {"$sort": {"analysis.created_at": -1}},
                {
                    "$group": {
                        "_id": "$_id",
                        "business": {"$first": "$$ROOT"},
                        "latest_analysis": {"$first": "$analysis"},
                    }
                },
                {
                    "$replaceRoot": {
                        "newRoot": {
                            "$mergeObjects": [
                                "$business",
                                {"analysis": "$latest_analysis"},
                            ]
                        }
                    }
                },
                {"$limit": limit},
            ]

            results = list(businesses_collection.aggregate(pipeline))
            return db._convert_documents(results)

        except Exception as e:
            logger.error(f"❌ Error retrieving businesses: {e}")
            return []

    def search_businesses(
        self, query: str, business_type: str = None
    ) -> List[Dict[str, Any]]:
        """Search businesses by name or description"""
        try:
            collection = db.get_collection("businesses")
            if collection is None:
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

            if businesses_collection is None or analyses_collection is None:
                return False

            from bson import ObjectId

            # Delete business
            business_result = businesses_collection.delete_one(
                {"_id": ObjectId(business_id)}
            )

            # Delete associated analysis
            analyses_collection.delete_many({"business_id": business_id})

            success = business_result.deleted_count > 0
            if success:
                logger.info(f"✅ Deleted business: {business_id}")
            return success

        except Exception as e:
            logger.error(f"❌ Error deleting business: {e}")
            return False

    async def _process_basic_analysis(self, business_data: BusinessInput) -> BusinessAnalysisResponse:
        """Basic analysis fallback when agents are not available"""
        try:
            print("⚠️ Using basic analysis fallback (agents not available)")
            
            # Create basic analysis using fallback responses
            strategic_plan = self._get_fallback_response("strategic", business_data.model_dump())
            creative_analysis = self._get_fallback_response("creative", business_data.model_dump())
            financial_analysis = self._get_fallback_response("financial", business_data.model_dump())
            sales_strategy = self._get_fallback_response("sales", business_data.model_dump())
            swot_analysis = self._get_fallback_response("swot", business_data.model_dump())
            bmc_analysis = self._get_fallback_response("business_model", business_data.model_dump())
            analytics_summary = self._get_fallback_response("analytics", business_data.model_dump())
            management_summary = self._get_fallback_response("manager", business_data.model_dump())

            # Generate overall recommendations
            overall_recommendations = self._generate_overall_recommendations(
                strategic_plan, creative_analysis, financial_analysis, sales_strategy,
                swot_analysis, bmc_analysis, analytics_summary
            )

            # Save to database
            business_id = self.save_business_data(
                business_data,
                {
                    "strategic_plan": strategic_plan,
                    "creative_analysis": creative_analysis,
                    "financial_analysis": financial_analysis,
                    "sales_strategy": sales_strategy,
                    "swot_analysis": swot_analysis,
                    "business_model_canvas": bmc_analysis,
                    "analytics_summary": analytics_summary,
                    "management_summary": management_summary,
                },
            )

            return BusinessAnalysisResponse(
                business_id=business_id,
                business_name=business_data.business_name,
                analysis_completed=True,
                strategic_plan=strategic_plan,
                creative_analysis=creative_analysis,
                financial_analysis=financial_analysis,
                sales_strategy=sales_strategy,
                swot_analysis=swot_analysis,
                business_model_canvas=bmc_analysis,
                analytics_summary=analytics_summary,
                management_summary=management_summary,
                overall_recommendations=overall_recommendations,
                task_assignments={},
                created_at=datetime.now().isoformat(),
            )

        except Exception as e:
            logger.error(f"Error in basic analysis: {e}")
            raise e


# Global service instance
business_service = BusinessService()
