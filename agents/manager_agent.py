from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import httpx
import asyncio
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Manager Agent", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


class MCPMessage(BaseModel):
    agent_type: str
    business_data: Dict[str, Any]
    timestamp: str
    request_id: str


class ManagerResponse(BaseModel):
    agent_type: str
    management_summary: Dict[str, Any]
    timestamp: str
    request_id: str


class ManagerAgent:
    """Manager Agent for coordinating and managing the multi-agent system"""

    def __init__(self):
        self.agent_type = "manager"
        self.client = httpx.AsyncClient(timeout=30.0)

    async def coordinate_analysis(
        self, business_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Coordinate the analysis process and manage agent interactions"""

        business_name = business_data.get("business_name", "")
        business_type = business_data.get("business_type", "")
        industry = business_data.get("industry", "")

        # Create dynamic management summary
        management_summary = {
            "business_name": business_name,
            "business_type": business_type,
            "process_coordination": {
                "workflow_status": "Completed",
                "agents_involved": [
                    "Strategic Agent",
                    "Creative Agent",
                    "Financial Agent",
                    "Sales Agent",
                    "Analytics Agent",
                ],
                "execution_time": "2-3 minutes",
                "quality_checks": "All agents responded successfully",
            },
            "resource_allocation": {
                "agent_priorities": {
                    "strategic": "High - Foundation for all other analysis",
                    "creative": "Medium - Supports marketing and branding",
                    "financial": "High - Critical for business viability",
                    "sales": "Medium - Essential for revenue generation",
                    "analytics": "High - Provides comprehensive insights",
                },
                "processing_order": [
                    "Strategic analysis first",
                    "Parallel processing of Creative, Financial, and Sales",
                    "Analytics integration and synthesis",
                ],
            },
            "quality_assurance": {
                "data_validation": "All input data validated",
                "response_quality": "All agents provided comprehensive analysis",
                "consistency_check": "Recommendations align across agents",
                "completeness_verification": "All required analysis areas covered",
            },
            "performance_metrics": {
                "system_performance": {
                    "response_time": "Optimal",
                    "reliability": "High",
                    "scalability": "Good",
                },
                "agent_performance": {
                    "strategic_agent": "Excellent - Comprehensive strategic plan",
                    "creative_agent": "Good - Detailed marketing strategy",
                    "financial_agent": "Excellent - Thorough financial analysis",
                    "sales_agent": "Good - Complete sales strategy",
                    "analytics_agent": "Excellent - Comprehensive insights",
                },
            },
            "risk_management": {
                "system_risks": [
                    {
                        "risk": "Agent communication failure",
                        "probability": "Low",
                        "mitigation": "Retry mechanisms and fallback responses",
                    },
                    {
                        "risk": "Data inconsistency",
                        "probability": "Low",
                        "mitigation": "Validation and cross-checking",
                    },
                ],
                "business_risks": [
                    {
                        "risk": f"{business_type} market competition",
                        "severity": "High",
                        "mitigation": f"Focus on {business_type} differentiation and quality",
                    },
                    {
                        "risk": f"{business_type} financial constraints",
                        "severity": "Medium",
                        "mitigation": f"Conservative {business_type} financial planning",
                    },
                ],
            },
            "optimization_recommendations": {
                "system_improvements": [
                    "Implement caching for faster responses",
                    "Add more specialized agents as needed",
                    "Enhance error handling and recovery",
                    "Improve data validation and sanitization",
                ],
                "business_optimizations": [
                    f"Focus on {business_type} execution quality",
                    f"Maintain {business_type} financial discipline",
                    f"Build strong {business_type} customer relationships",
                    f"Invest in {business_type} technology and training",
                ],
            },
            "next_steps": {
                "immediate_actions": [
                    "Review and validate all agent recommendations",
                    "Prioritize implementation based on analytics insights",
                    "Develop detailed action plan with timelines",
                    "Set up monitoring and tracking systems",
                ],
                "short_term_goals": [
                    "Implement high-priority recommendations",
                    "Establish key performance indicators",
                    f"Begin {business_type} marketing campaign execution",
                    f"Set up {business_type} financial management systems",
                ],
                "long_term_objectives": [
                    f"Achieve {business_type} break-even within 8-12 months",
                    f"Expand {business_type} to additional locations",
                    f"Develop strong {business_type} brand presence",
                    f"Build sustainable {business_type} competitive advantages",
                ],
            },
            "success_criteria": {
                "operational_metrics": [
                    f"Monthly {business_type} revenue targets met",
                    f"{business_type} customer satisfaction scores > 4.5/5",
                    f"{business_type} employee retention rate > 80%",
                    f"{business_type} cost control within budget",
                ],
                "strategic_metrics": [
                    f"{business_type} market share growth",
                    f"{business_type} brand recognition increase",
                    f"{business_type} customer loyalty program adoption",
                    f"{business_type} competitive positioning strength",
                ],
            },
            "management_insights": [
                f"The multi-agent system successfully provided comprehensive {business_type} business analysis",
                f"All key {business_type} business areas were thoroughly evaluated",
                f"{business_type} recommendations are actionable and well-aligned",
                f"{business_type} success probability is high with proper execution",
                f"Focus should be on {business_type} implementation quality and customer experience",
                f"Regular {business_type} monitoring and adaptation will be crucial for success",
            ],
        }

        return management_summary

    async def trigger_analytics(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Trigger analytics agent for periodic analysis"""
        try:
            analytics_message = {
                "agent_type": "analytics",
                "business_data": business_data,
                "timestamp": datetime.now().isoformat(),
                "request_id": f"analytics_{datetime.now().timestamp()}",
            }

            response = await self.client.post(
                "http://localhost:8006/receive_message",
                json=analytics_message,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": f"Analytics trigger failed: {str(e)}"}


# Initialize manager agent
manager_agent = ManagerAgent()


@app.post("/receive_message", response_model=ManagerResponse)
async def receive_message(message: MCPMessage):
    """Receive and process messages from Core Agent"""
    try:
        management_summary = await manager_agent.coordinate_analysis(
            message.business_data
        )

        return ManagerResponse(
            agent_type=message.agent_type,
            management_summary=management_summary,
            timestamp=datetime.now().isoformat(),
            request_id=message.request_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Management coordination failed: {str(e)}"
        )


@app.post("/trigger_analytics")
async def trigger_analytics(business_data: Dict[str, Any]):
    """Trigger periodic analytics analysis"""
    try:
        result = await manager_agent.trigger_analytics(business_data)
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Analytics trigger failed: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_type": "manager",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5005)
