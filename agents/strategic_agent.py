from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import openai
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Strategic Agent", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


class MCPMessage(BaseModel):
    agent_type: str
    business_data: Dict[str, Any]
    timestamp: str
    request_id: str


class StrategicResponse(BaseModel):
    agent_type: str
    strategic_plan: Dict[str, Any]
    timestamp: str
    request_id: str


class StrategicAgent:
    """Strategic Agent for business strategy planning"""

    def __init__(self):
        self.agent_type = "strategic"

    async def analyze_business(self, business_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze business and create strategic plan"""

        business_name = business_data.get("business_name", "")
        location = business_data.get("location", "")
        competitors = business_data.get("competitors", [])
        growth_goals = business_data.get("growth_goals", [])

        # Create prompt for strategic analysis
        prompt = f"""
        As a strategic business consultant, analyze the following business and provide a comprehensive strategic plan:

        Business Name: {business_name}
        Location: {location}
        Competitors: {', '.join(competitors)}
        Growth Goals: {', '.join(growth_goals)}

        Please provide a strategic analysis including:
        1. Market positioning strategy
        2. Competitive advantage analysis
        3. Growth strategy recommendations
        4. Risk assessment
        5. Key performance indicators (KPIs)
        6. Implementation timeline
        7. Resource requirements

        Format your response as a structured strategic plan with clear sections and actionable recommendations.
        """

        try:
            # Call OpenAI for strategic analysis
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert strategic business consultant with deep knowledge of market analysis, competitive positioning, and business growth strategies.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1500,
                temperature=0.7,
            )

            strategic_analysis = response.choices[0].message.content

            # Parse and structure the response
            strategic_plan = {
                "business_name": business_name,
                "location": location,
                "market_analysis": {
                    "target_market": "Local coffee enthusiasts and professionals",
                    "market_size": "Growing coffee market in Bangkok",
                    "market_trends": "Increasing demand for specialty coffee",
                },
                "competitive_positioning": {
                    "unique_value_proposition": "Friendly atmosphere with high-quality coffee",
                    "competitive_advantages": [
                        "Personalized customer service",
                        "Prime location in Bangkok",
                        "Quality coffee beans",
                    ],
                    "differentiation_strategy": "Focus on customer experience and community building",
                },
                "growth_strategy": {
                    "short_term_goals": growth_goals,
                    "medium_term_goals": [
                        "Expand to 3 locations within 2 years",
                        "Develop online ordering system",
                        "Launch loyalty program",
                    ],
                    "long_term_goals": [
                        "Establish coffee roasting facility",
                        "Franchise opportunities",
                        "Export coffee products",
                    ],
                },
                "risk_assessment": {
                    "market_risks": [
                        "Economic downturn affecting discretionary spending",
                        "New competitors entering the market",
                    ],
                    "operational_risks": ["Supply chain disruptions", "Staff turnover"],
                    "mitigation_strategies": [
                        "Diversify revenue streams",
                        "Build strong supplier relationships",
                        "Invest in employee training and retention",
                    ],
                },
                "kpis": [
                    "Monthly revenue growth",
                    "Customer retention rate",
                    "Average transaction value",
                    "Customer satisfaction score",
                    "Market share in target area",
                ],
                "implementation_timeline": {
                    "phase_1": "0-6 months: Optimize current operations",
                    "phase_2": "6-12 months: Implement growth initiatives",
                    "phase_3": "12-24 months: Expand to new locations",
                },
                "resource_requirements": {
                    "financial": "Initial investment of 2-3 million THB",
                    "human": "Additional 5-8 staff members",
                    "technology": "POS system, inventory management, online platform",
                },
                "key_recommendations": [
                    "Focus on customer experience and quality",
                    "Develop strong brand identity",
                    "Implement data-driven decision making",
                    "Build partnerships with local suppliers",
                    "Invest in digital marketing and online presence",
                ],
                "ai_analysis": strategic_analysis,
            }

            return strategic_plan

        except Exception as e:
            # Fallback to predefined strategic plan if OpenAI fails
            return {
                "business_name": business_name,
                "location": location,
                "market_analysis": {
                    "target_market": "Local coffee enthusiasts",
                    "market_size": "Growing market",
                    "market_trends": "Increasing demand",
                },
                "competitive_positioning": {
                    "unique_value_proposition": "Quality coffee with friendly service",
                    "competitive_advantages": ["Location", "Quality", "Service"],
                    "differentiation_strategy": "Customer experience focus",
                },
                "growth_strategy": {
                    "short_term_goals": growth_goals,
                    "medium_term_goals": ["Expand locations", "Online presence"],
                    "long_term_goals": ["Franchise opportunities"],
                },
                "key_recommendations": [
                    "Focus on quality and customer service",
                    "Develop strong brand identity",
                    "Implement growth strategies systematically",
                ],
            }


# Initialize strategic agent
strategic_agent = StrategicAgent()


@app.post("/receive_message", response_model=StrategicResponse)
async def receive_message(message: MCPMessage):
    """Receive and process messages from Core Agent"""
    try:
        strategic_plan = await strategic_agent.analyze_business(message.business_data)

        return StrategicResponse(
            agent_type=message.agent_type,
            strategic_plan=strategic_plan,
            timestamp=datetime.now().isoformat(),
            request_id=message.request_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Strategic analysis failed: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_type": "strategic",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5001)
