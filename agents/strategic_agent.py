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
        business_type = business_data.get("business_type", "")
        location = business_data.get("location", "")
        description = business_data.get("description", "")
        target_market = business_data.get("target_market", "")
        competitors = business_data.get("competitors", [])
        growth_goals = business_data.get("growth_goals", [])
        industry = business_data.get("industry", "")
        business_model = business_data.get("business_model", "")
        market_size = business_data.get("market_size", "")
        unique_value_proposition = business_data.get("unique_value_proposition", "")
        initial_investment = business_data.get("initial_investment")
        team_size = business_data.get("team_size")

        # Create dynamic prompt for strategic analysis
        prompt = f"""
        As a strategic business consultant, analyze the following business and provide a comprehensive strategic plan:

        Business Information:
        - Name: {business_name}
        - Type: {business_type}
        - Location: {location}
        - Description: {description}
        - Target Market: {target_market}
        - Industry: {industry}
        - Business Model: {business_model}
        - Market Size: {market_size}
        - Unique Value Proposition: {unique_value_proposition}
        - Initial Investment: ${initial_investment:,.0f}" if initial_investment else "Not specified"
        - Team Size: {team_size} employees" if team_size else "Not specified"
        - Competitors: {', '.join(competitors)}
        - Growth Goals: {', '.join(growth_goals)}

        Please provide a comprehensive strategic analysis specifically tailored for this {business_type} business, including:

        1. Market Analysis:
           - Target market assessment
           - Market size and growth potential
           - Market trends and opportunities

        2. Competitive Positioning:
           - Unique value proposition analysis
           - Competitive advantages
           - Differentiation strategy

        3. Growth Strategy:
           - Short-term goals (0-12 months)
           - Medium-term goals (1-3 years)
           - Long-term goals (3-5 years)

        4. Risk Assessment:
           - Market risks
           - Operational risks
           - Mitigation strategies

        5. Key Performance Indicators (KPIs):
           - Revenue metrics
           - Customer metrics
           - Operational metrics

        6. Implementation Timeline:
           - Phase 1 (0-6 months)
           - Phase 2 (6-12 months)
           - Phase 3 (12-24 months)

        7. Resource Requirements:
           - Financial requirements
           - Human resources
           - Technology needs

        Focus on providing specific, actionable recommendations that are relevant to this particular business type and industry.
        """

        try:
            # Call OpenAI for strategic analysis
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert strategic business consultant with deep knowledge of {industry} industry, market analysis, competitive positioning, and business growth strategies. Provide specific, actionable advice tailored to {business_type} businesses.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2000,
                temperature=0.7,
            )

            strategic_analysis = response.choices[0].message.content

            # Create dynamic strategic plan structure
            strategic_plan = {
                "business_name": business_name,
                "business_type": business_type,
                "location": location,
                "market_analysis": {
                    "target_market": target_market,
                    "market_size": market_size or "To be determined",
                    "market_trends": f"Industry-specific trends for {industry}",
                },
                "competitive_positioning": {
                    "unique_value_proposition": unique_value_proposition
                    or f"Quality {business_type} services",
                    "competitive_advantages": [
                        f"Specialized {business_type} expertise",
                        f"Strong market positioning in {location}",
                        "Customer-focused approach",
                    ],
                    "differentiation_strategy": f"Focus on {business_type} excellence and customer experience",
                },
                "growth_strategy": {
                    "short_term_goals": growth_goals,
                    "medium_term_goals": [
                        f"Expand {business_type} operations",
                        "Develop online presence",
                        "Build customer loyalty program",
                    ],
                    "long_term_goals": [
                        f"Establish {business_type} market leadership",
                        "Explore franchise opportunities",
                        "Expand to new markets",
                    ],
                },
                "risk_assessment": {
                    "market_risks": [
                        "Economic downturn affecting customer spending",
                        "New competitors entering the market",
                        f"Industry-specific regulatory changes",
                    ],
                    "operational_risks": [
                        "Supply chain disruptions",
                        "Staff turnover and training",
                        "Technology infrastructure challenges",
                    ],
                    "mitigation_strategies": [
                        "Diversify revenue streams",
                        "Build strong supplier relationships",
                        "Invest in employee training and retention",
                        "Implement robust technology systems",
                    ],
                },
                "kpis": [
                    "Monthly revenue growth",
                    "Customer acquisition cost",
                    "Customer lifetime value",
                    "Customer satisfaction score",
                    f"{business_type} specific metrics",
                ],
                "implementation_timeline": {
                    "phase_1": "0-6 months: Optimize current operations and establish foundation",
                    "phase_2": "6-12 months: Implement growth initiatives and expand market presence",
                    "phase_3": "12-24 months: Scale operations and explore new opportunities",
                },
                "resource_requirements": {
                    "financial": (
                        f"Initial investment of ${initial_investment:,.0f}"
                        if initial_investment
                        else "Investment requirements to be determined"
                    ),
                    "human": (
                        f"{team_size + 5 if team_size else 10} staff members"
                        if team_size
                        else "Team size to be determined"
                    ),
                    "technology": f"{business_type} specific technology and systems",
                },
                "key_recommendations": [
                    f"Focus on {business_type} quality and customer experience",
                    "Develop strong brand identity and market positioning",
                    "Implement data-driven decision making",
                    "Build strategic partnerships and supplier relationships",
                    "Invest in digital marketing and online presence",
                    f"Stay updated with {industry} industry trends",
                ],
                "ai_analysis": strategic_analysis,
            }

            return strategic_plan

        except Exception as e:
            # Fallback to dynamic strategic plan if OpenAI fails
            return {
                "business_name": business_name,
                "business_type": business_type,
                "location": location,
                "market_analysis": {
                    "target_market": target_market or f"{business_type} customers",
                    "market_size": market_size or "Growing market",
                    "market_trends": f"Positive trends in {industry}",
                },
                "competitive_positioning": {
                    "unique_value_proposition": unique_value_proposition
                    or f"Quality {business_type} services",
                    "competitive_advantages": ["Location", "Quality", "Service"],
                    "differentiation_strategy": f"Focus on {business_type} excellence",
                },
                "growth_strategy": {
                    "short_term_goals": growth_goals,
                    "medium_term_goals": [
                        f"Expand {business_type} operations",
                        "Develop online presence",
                    ],
                    "long_term_goals": [f"Establish {business_type} market leadership"],
                },
                "key_recommendations": [
                    f"Focus on {business_type} quality and customer service",
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
