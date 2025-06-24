from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import httpx
import asyncio
import json
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Multi-Agent Business Analysis System", version="1.0.0")


# Business input model
class BusinessInput(BaseModel):
    business_name: str
    location: str
    competitors: List[str]
    growth_goals: List[str]


# Response model
class BusinessAnalysisResponse(BaseModel):
    business_name: str
    timestamp: str
    strategic_plan: Dict[str, Any]
    creative_analysis: Dict[str, Any]
    financial_analysis: Dict[str, Any]
    sales_strategy: Dict[str, Any]
    swot_analysis: Dict[str, Any]
    business_model_canvas: Dict[str, Any]
    analytics_summary: Dict[str, Any]
    overall_recommendations: List[str]


# Agent configuration
AGENT_CONFIG = {
    "strategic": {"url": "http://localhost:5001", "port": 5001},
    "creative": {"url": "http://localhost:5002", "port": 5002},
    "financial": {"url": "http://localhost:5003", "port": 5003},
    "sales": {"url": "http://localhost:5004", "port": 5004},
    "manager": {"url": "http://localhost:5005", "port": 5005},
    "analytics": {"url": "http://localhost:5006", "port": 5006},
    "swot": {"url": "http://localhost:5007", "port": 5007},
    "business_model": {"url": "http://localhost:5008", "port": 5008},
}


class MCPClient:
    """MCP Client for communicating with agent servers"""

    def __init__(self):
        self.client = httpx.AsyncClient(timeout=30.0)

    async def send_message(
        self, agent_url: str, message: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Send message to agent via MCP"""
        try:
            response = await self.client.post(
                f"{agent_url}/receive_message",
                json=message,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to communicate with agent: {str(e)}"
            )
        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=f"Agent error: {e.response.text}",
            )


class CoreAgent:
    """Core Agent that orchestrates the multi-agent system"""

    def __init__(self):
        self.mcp_client = MCPClient()

    async def process_business_request(
        self, business_data: BusinessInput
    ) -> BusinessAnalysisResponse:
        """Main processing logic for business analysis"""

        # Step 1: Send to Strategic Agent
        strategic_message = {
            "agent_type": "strategic",
            "business_data": business_data.dict(),
            "timestamp": datetime.now().isoformat(),
            "request_id": f"req_{datetime.now().timestamp()}",
        }

        strategic_response = await self.mcp_client.send_message(
            AGENT_CONFIG["strategic"]["url"], strategic_message
        )

        # Step 2: Send to SWOT Agent (can run in parallel with other agents)
        swot_message = {
            "agent_type": "swot",
            "business_data": business_data.dict(),
            "strategic_plan": strategic_response.get("strategic_plan", {}),
            "timestamp": datetime.now().isoformat(),
            "request_id": f"req_{datetime.now().timestamp()}",
        }

        swot_response = await self.mcp_client.send_message(
            AGENT_CONFIG["swot"]["url"], swot_message
        )

        # Step 3: Send to Business Model Canvas Agent (uses SWOT analysis)
        bmc_message = {
            "agent_type": "business_model",
            "business_data": business_data.dict(),
            "strategic_plan": strategic_response.get("strategic_plan", {}),
            "swot_analysis": swot_response.get("swot_analysis", {}),
            "timestamp": datetime.now().isoformat(),
            "request_id": f"req_{datetime.now().timestamp()}",
        }

        bmc_response = await self.mcp_client.send_message(
            AGENT_CONFIG["business_model"]["url"], bmc_message
        )

        # Step 4: Send to other agents in parallel
        agent_tasks = []

        # Creative Agent
        creative_message = {
            "agent_type": "creative",
            "business_data": business_data.dict(),
            "strategic_plan": strategic_response.get("strategic_plan", {}),
            "timestamp": datetime.now().isoformat(),
            "request_id": f"req_{datetime.now().timestamp()}",
        }
        agent_tasks.append(
            self.mcp_client.send_message(
                AGENT_CONFIG["creative"]["url"], creative_message
            )
        )

        # Financial Agent
        financial_message = {
            "agent_type": "financial",
            "business_data": business_data.dict(),
            "strategic_plan": strategic_response.get("strategic_plan", {}),
            "timestamp": datetime.now().isoformat(),
            "request_id": f"req_{datetime.now().timestamp()}",
        }
        agent_tasks.append(
            self.mcp_client.send_message(
                AGENT_CONFIG["financial"]["url"], financial_message
            )
        )

        # Sales Agent
        sales_message = {
            "agent_type": "sales",
            "business_data": business_data.dict(),
            "strategic_plan": strategic_response.get("strategic_plan", {}),
            "timestamp": datetime.now().isoformat(),
            "request_id": f"req_{datetime.now().timestamp()}",
        }
        agent_tasks.append(
            self.mcp_client.send_message(AGENT_CONFIG["sales"]["url"], sales_message)
        )

        # Execute all agent tasks in parallel
        agent_responses = await asyncio.gather(*agent_tasks)
        creative_response, financial_response, sales_response = agent_responses

        # Step 5: Trigger Analytics with all data
        analytics_message = {
            "agent_type": "analytics",
            "business_data": business_data.dict(),
            "strategic_plan": strategic_response.get("strategic_plan", {}),
            "creative_analysis": creative_response.get("creative_analysis", {}),
            "financial_analysis": financial_response.get("financial_analysis", {}),
            "sales_strategy": sales_response.get("sales_strategy", {}),
            "swot_analysis": swot_response.get("swot_analysis", {}),
            "business_model_canvas": bmc_response.get("business_model_canvas", {}),
            "timestamp": datetime.now().isoformat(),
            "request_id": f"req_{datetime.now().timestamp()}",
        }

        analytics_response = await self.mcp_client.send_message(
            AGENT_CONFIG["analytics"]["url"], analytics_message
        )

        # Step 6: Generate overall recommendations
        overall_recommendations = self._generate_overall_recommendations(
            strategic_response,
            creative_response,
            financial_response,
            sales_response,
            swot_response,
            bmc_response,
            analytics_response,
        )

        # Step 7: Return aggregated response
        return BusinessAnalysisResponse(
            business_name=business_data.business_name,
            timestamp=datetime.now().isoformat(),
            strategic_plan=strategic_response.get("strategic_plan", {}),
            creative_analysis=creative_response.get("creative_analysis", {}),
            financial_analysis=financial_response.get("financial_analysis", {}),
            sales_strategy=sales_response.get("sales_strategy", {}),
            swot_analysis=swot_response.get("swot_analysis", {}),
            business_model_canvas=bmc_response.get("business_model_canvas", {}),
            analytics_summary=analytics_response.get("analytics_summary", {}),
            overall_recommendations=overall_recommendations,
        )

    def _generate_overall_recommendations(
        self, strategic, creative, financial, sales, swot, bmc, analytics
    ):
        """Generate overall recommendations based on all agent outputs"""
        recommendations = []

        # Add strategic recommendations
        if strategic.get("strategic_plan", {}).get("key_recommendations"):
            recommendations.extend(strategic["strategic_plan"]["key_recommendations"])

        # Add creative recommendations
        if creative.get("creative_analysis", {}).get("recommendations"):
            recommendations.extend(creative["creative_analysis"]["recommendations"])

        # Add financial recommendations
        if financial.get("financial_analysis", {}).get("recommendations"):
            recommendations.extend(financial["financial_analysis"]["recommendations"])

        # Add sales recommendations
        if sales.get("sales_strategy", {}).get("recommendations"):
            recommendations.extend(sales["sales_strategy"]["recommendations"])

        # Add SWOT action plan
        if (
            swot.get("swot_analysis", {})
            .get("action_plan", {})
            .get("immediate_actions")
        ):
            recommendations.extend(
                swot["swot_analysis"]["action_plan"]["immediate_actions"]
            )

        # Add Business Model Canvas insights
        if (
            bmc.get("business_model_canvas", {})
            .get("canvas_insights", {})
            .get("strategic_recommendations")
        ):
            recommendations.extend(
                bmc["business_model_canvas"]["canvas_insights"][
                    "strategic_recommendations"
                ]
            )

        # Add analytics insights
        if analytics.get("analytics_summary", {}).get("key_insights"):
            recommendations.extend(analytics["analytics_summary"]["key_insights"])

        return list(set(recommendations))  # Remove duplicates


# Initialize core agent
core_agent = CoreAgent()


@app.post("/process-business", response_model=BusinessAnalysisResponse)
async def process_business(business_input: BusinessInput):
    """
    Process business analysis request through multi-agent system
    """
    try:
        result = await core_agent.process_business_request(business_input)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Multi-Agent Business Analysis System",
        "version": "1.0.0",
        "endpoints": {"process_business": "/process-business", "health": "/health"},
        "agents": {
            "strategic": "Port 5001",
            "creative": "Port 5002",
            "financial": "Port 5003",
            "sales": "Port 5004",
            "manager": "Port 5005",
            "analytics": "Port 5006",
            "swot": "Port 5007",
            "business_model": "Port 5008",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5099)
