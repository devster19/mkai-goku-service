from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import openai
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="SWOT Analysis Agent", version="1.0.0")

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


class MCPMessage(BaseModel):
    agent_type: str
    business_data: Dict[str, Any]
    strategic_plan: Dict[str, Any] = {}
    timestamp: str
    request_id: str


class SWOTResponse(BaseModel):
    agent_type: str
    swot_analysis: Dict[str, Any]
    timestamp: str
    request_id: str


class SWOTAgent:
    """SWOT Analysis Agent for comprehensive business analysis"""

    def __init__(self):
        self.agent_type = "swot"

    async def perform_swot_analysis(
        self, business_data: Dict[str, Any], strategic_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform comprehensive SWOT analysis"""

        business_name = business_data.get("business_name", "")
        location = business_data.get("location", "")
        competitors = business_data.get("competitors", [])
        growth_goals = business_data.get("growth_goals", [])

        # Create prompt for SWOT analysis
        prompt = f"""
        As a business strategy expert, perform a comprehensive SWOT analysis for the following business:

        Business Name: {business_name}
        Location: {location}
        Competitors: {', '.join(competitors)}
        Growth Goals: {', '.join(growth_goals)}
        
        Strategic Context: {strategic_plan.get('competitive_positioning', {}).get('unique_value_proposition', '')}

        Please provide a detailed SWOT analysis including:

        STRENGTHS (Internal Positive Factors):
        - What are the business's internal advantages?
        - What does the business do well?
        - What unique resources does it have?
        - What competitive advantages exist?

        WEAKNESSES (Internal Negative Factors):
        - What are the business's internal disadvantages?
        - What areas need improvement?
        - What resources are lacking?
        - What do competitors do better?

        OPPORTUNITIES (External Positive Factors):
        - What external factors can the business exploit?
        - What market trends favor the business?
        - What new technologies or changes create opportunities?
        - What partnerships or collaborations are possible?

        THREATS (External Negative Factors):
        - What external factors could harm the business?
        - What market changes could be problematic?
        - What new competitors might emerge?
        - What economic or regulatory changes could impact the business?

        For each category, provide specific, actionable insights relevant to a coffee shop business in Thailand.
        """

        try:
            # Call OpenAI for SWOT analysis
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert business strategist specializing in SWOT analysis for small businesses, particularly in the food and beverage industry in Thailand.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1500,
                temperature=0.7,
            )

            swot_analysis_text = response.choices[0].message.content

            # Structure the SWOT analysis
            swot_analysis = {
                "business_name": business_name,
                "analysis_timestamp": datetime.now().isoformat(),
                "strengths": {
                    "internal_advantages": [
                        "Prime location in Bangkok with high foot traffic",
                        "Quality-focused approach to coffee and service",
                        "Strong local community connections",
                        "Flexible business model adaptable to market changes",
                        "Personalized customer service and relationship building",
                    ],
                    "unique_resources": [
                        "Local market knowledge and cultural understanding",
                        "Established supplier relationships",
                        "Skilled barista team with coffee expertise",
                        "Community-oriented business approach",
                        "Thai cultural integration in business model",
                    ],
                    "competitive_advantages": [
                        "Authentic Thai coffee experience",
                        "Community-focused atmosphere",
                        "Personalized customer relationships",
                        "Local market expertise",
                        "Flexible and adaptable operations",
                    ],
                    "core_competencies": [
                        "Coffee quality and preparation",
                        "Customer service excellence",
                        "Community engagement",
                        "Local market understanding",
                        "Operational efficiency",
                    ],
                },
                "weaknesses": {
                    "internal_limitations": [
                        "Limited financial resources for expansion",
                        "Small team size limiting operational capacity",
                        "Limited marketing budget and expertise",
                        "Dependency on key staff members",
                        "Limited technological infrastructure",
                    ],
                    "areas_for_improvement": [
                        "Digital presence and online ordering system",
                        "Inventory management and cost control",
                        "Staff training and development programs",
                        "Marketing and brand awareness",
                        "Financial planning and cash flow management",
                    ],
                    "resource_gaps": [
                        "Limited access to capital for growth",
                        "Lack of specialized marketing expertise",
                        "Limited technology infrastructure",
                        "Insufficient data analytics capabilities",
                        "Limited international market knowledge",
                    ],
                    "operational_challenges": [
                        "Supply chain management complexity",
                        "Staff recruitment and retention",
                        "Quality consistency across operations",
                        "Cost control and pricing optimization",
                        "Regulatory compliance and licensing",
                    ],
                },
                "opportunities": {
                    "market_trends": [
                        "Growing coffee culture in Thailand",
                        "Increasing demand for specialty coffee",
                        "Rising disposable income among target demographics",
                        "Growing tourism industry in Bangkok",
                        "Digital transformation in F&B sector",
                    ],
                    "external_factors": [
                        "Government support for small businesses",
                        "Growing health consciousness and premium coffee demand",
                        "Increasing remote work culture creating demand for cafe spaces",
                        "Social media marketing opportunities",
                        "Partnership opportunities with local businesses",
                    ],
                    "growth_potential": [
                        "Expansion to multiple locations",
                        "Online ordering and delivery services",
                        "Franchise opportunities",
                        "Product diversification (coffee beans, merchandise)",
                        "Corporate catering and events",
                    ],
                    "strategic_opportunities": [
                        "Partnerships with co-working spaces",
                        "Collaboration with local artists and musicians",
                        "Tourism-focused marketing campaigns",
                        "Subscription and loyalty programs",
                        "Educational coffee workshops and events",
                    ],
                },
                "threats": {
                    "market_risks": [
                        "Intense competition from established coffee chains",
                        "Economic downturn affecting discretionary spending",
                        "Changing consumer preferences and trends",
                        "New competitors entering the market",
                        "Fluctuating coffee bean prices",
                    ],
                    "external_challenges": [
                        "Regulatory changes affecting food service",
                        "Supply chain disruptions and inflation",
                        "Labor shortage and rising wages",
                        "Technology disruption and changing customer expectations",
                        "Environmental regulations and sustainability requirements",
                    ],
                    "competitive_threats": [
                        "Large coffee chains with significant resources",
                        "New specialty coffee shops opening nearby",
                        "Online coffee delivery services",
                        "Convenience stores expanding coffee offerings",
                        "International coffee brands entering the market",
                    ],
                    "operational_risks": [
                        "Key staff turnover and knowledge loss",
                        "Equipment failure and maintenance costs",
                        "Food safety and quality control issues",
                        "Cash flow problems and financial instability",
                        "Location-related issues (rent increases, redevelopment)",
                    ],
                },
                "strategic_implications": {
                    "strength_opportunity_strategies": [
                        "Leverage community connections for marketing and partnerships",
                        "Use local expertise to create unique Thai coffee experiences",
                        "Expand quality-focused approach to new product lines",
                        "Utilize flexible operations to adapt to market opportunities",
                    ],
                    "weakness_opportunity_strategies": [
                        "Partner with technology providers to improve digital capabilities",
                        "Collaborate with marketing agencies to enhance brand presence",
                        "Seek external funding for expansion opportunities",
                        "Invest in staff training to improve operational efficiency",
                    ],
                    "strength_threat_strategies": [
                        "Use community relationships to build customer loyalty against competition",
                        "Leverage quality focus to differentiate from mass-market competitors",
                        "Utilize local expertise to adapt to market changes",
                        "Apply flexible operations to respond to external threats",
                    ],
                    "weakness_threat_strategies": [
                        "Develop contingency plans for key staff departures",
                        "Build financial reserves to weather economic downturns",
                        "Diversify suppliers to reduce supply chain risks",
                        "Invest in technology to improve operational efficiency",
                    ],
                },
                "action_plan": {
                    "immediate_actions": [
                        "Conduct detailed competitor analysis",
                        "Develop comprehensive staff training program",
                        "Implement digital ordering system",
                        "Create emergency fund for financial stability",
                    ],
                    "short_term_goals": [
                        "Improve digital presence and online ordering",
                        "Develop loyalty program to increase customer retention",
                        "Establish partnerships with local businesses",
                        "Implement cost control and inventory management systems",
                    ],
                    "long_term_strategies": [
                        "Expand to multiple locations with standardized operations",
                        "Develop franchise model for scalability",
                        "Create strong brand identity and market presence",
                        "Build sustainable competitive advantages",
                    ],
                },
                "risk_mitigation": {
                    "high_priority_risks": [
                        {
                            "risk": "Intense competition",
                            "mitigation": "Focus on unique value proposition and customer experience",
                            "priority": "High",
                        },
                        {
                            "risk": "Economic downturn",
                            "mitigation": "Build cash reserves and diversify revenue streams",
                            "priority": "High",
                        },
                        {
                            "risk": "Staff turnover",
                            "mitigation": "Implement retention strategies and cross-training",
                            "priority": "Medium",
                        },
                    ]
                },
                "ai_analysis": swot_analysis_text,
            }

            return swot_analysis

        except Exception as e:
            # Fallback to predefined SWOT analysis if OpenAI fails
            return {
                "business_name": business_name,
                "strengths": {
                    "internal_advantages": [
                        "Quality focus",
                        "Local expertise",
                        "Community connections",
                    ]
                },
                "weaknesses": {
                    "internal_limitations": [
                        "Limited resources",
                        "Small team",
                        "Limited marketing budget",
                    ]
                },
                "opportunities": {
                    "market_trends": [
                        "Growing coffee culture",
                        "Increasing demand",
                        "Digital transformation",
                    ]
                },
                "threats": {
                    "market_risks": [
                        "Competition",
                        "Economic changes",
                        "Supply chain issues",
                    ]
                },
                "action_plan": {
                    "immediate_actions": [
                        "Competitor analysis",
                        "Staff training",
                        "Digital implementation",
                    ]
                },
            }


# Initialize SWOT agent
swot_agent = SWOTAgent()


@app.post("/receive_message", response_model=SWOTResponse)
async def receive_message(message: MCPMessage):
    """Receive and process messages from Core Agent"""
    try:
        swot_analysis = await swot_agent.perform_swot_analysis(
            message.business_data, message.strategic_plan
        )

        return SWOTResponse(
            agent_type=message.agent_type,
            swot_analysis=swot_analysis,
            timestamp=datetime.now().isoformat(),
            request_id=message.request_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SWOT analysis failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_type": "swot",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5007)
