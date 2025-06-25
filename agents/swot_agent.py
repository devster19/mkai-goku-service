from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import openai
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="SWOT Analysis Agent", version="1.0.0")

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

        # Create dynamic prompt for SWOT analysis
        prompt = f"""
        As a business strategy expert, perform a comprehensive SWOT analysis for the following business:

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
        
        Strategic Context: {strategic_plan.get('competitive_positioning', {}).get('unique_value_proposition', '')}

        Please provide a detailed SWOT analysis specifically tailored for this {business_type} business in the {industry} industry.
        """

        try:
            # Call OpenAI for SWOT analysis
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert business strategist specializing in SWOT analysis for {business_type} businesses in the {industry} industry. Provide specific, actionable insights tailored to this business type and industry.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2000,
                temperature=0.7,
            )

            swot_analysis_text = response.choices[0].message.content

            # Create dynamic SWOT analysis structure
            swot_analysis = {
                "business_name": business_name,
                "business_type": business_type,
                "analysis_timestamp": datetime.now().isoformat(),
                "strengths": {
                    "internal_advantages": [
                        f"Strong {business_type} expertise and knowledge",
                        f"Quality-focused approach to {business_type} services",
                        f"Strategic location in {location}",
                        "Flexible business model adaptable to market changes",
                        "Personalized customer service and relationship building",
                    ],
                    "unique_resources": [
                        f"Specialized {business_type} knowledge and skills",
                        f"Established {industry} industry relationships",
                        f"Skilled team with {business_type} expertise",
                        f"Industry-specific business approach",
                        f"Local market understanding in {location}",
                    ],
                    "competitive_advantages": [
                        f"Authentic {business_type} experience",
                        f"Industry-focused expertise",
                        "Personalized customer relationships",
                        f"Local market knowledge in {location}",
                        "Flexible and adaptable operations",
                    ],
                    "core_competencies": [
                        f"{business_type} quality and service delivery",
                        "Customer service excellence",
                        f"{industry} industry expertise",
                        "Local market understanding",
                        "Operational efficiency",
                    ],
                },
                "weaknesses": {
                    "internal_limitations": [
                        "Limited financial resources for expansion",
                        f"Small team size limiting {business_type} operational capacity",
                        "Limited marketing budget and expertise",
                        "Dependency on key staff members",
                        "Limited technological infrastructure",
                    ],
                    "areas_for_improvement": [
                        f"Digital presence and {business_type} online services",
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
                        f"Limited {industry} industry knowledge",
                    ],
                    "operational_challenges": [
                        f"{business_type} supply chain management complexity",
                        "Staff recruitment and retention",
                        f"{business_type} quality consistency across operations",
                        "Cost control and pricing optimization",
                        f"{industry} regulatory compliance and licensing",
                    ],
                },
                "opportunities": {
                    "market_trends": [
                        f"Growing {business_type} market demand",
                        f"Increasing demand for quality {business_type} services",
                        f"Rising disposable income among {target_market}",
                        f"Growing {industry} industry in {location}",
                        f"Digital transformation in {industry} sector",
                    ],
                    "external_factors": [
                        "Government support for small businesses",
                        f"Growing demand for {business_type} services",
                        f"Increasing {industry} industry opportunities",
                        "Social media marketing opportunities",
                        f"Partnership opportunities in {industry}",
                    ],
                    "growth_potential": [
                        f"Expansion of {business_type} operations",
                        f"Online {business_type} services and delivery",
                        f"Franchise opportunities in {business_type}",
                        f"Product diversification in {industry}",
                        f"Corporate {business_type} services",
                    ],
                    "strategic_opportunities": [
                        f"Partnerships with {industry} businesses",
                        f"Collaboration with {business_type} experts",
                        f"{industry}-focused marketing campaigns",
                        f"Subscription and loyalty programs for {business_type}",
                        f"Educational {business_type} workshops and events",
                    ],
                },
                "threats": {
                    "market_risks": [
                        f"Intense competition from established {business_type} providers",
                        "Economic downturn affecting customer spending",
                        f"Changing {industry} industry preferences and trends",
                        f"New {business_type} competitors entering the market",
                        f"Fluctuating {industry} industry costs",
                    ],
                    "external_challenges": [
                        f"Regulatory changes affecting {industry}",
                        f"{business_type} supply chain disruptions and inflation",
                        "Labor shortage and rising wages",
                        "Technology disruption and changing customer expectations",
                        f"Environmental regulations affecting {industry}",
                    ],
                    "competitive_threats": [
                        f"Large {business_type} companies with significant resources",
                        f"New {business_type} providers opening nearby",
                        f"Online {business_type} service platforms",
                        f"Established companies expanding {business_type} offerings",
                        f"International {business_type} brands entering the market",
                    ],
                    "operational_risks": [
                        "Key staff turnover and knowledge loss",
                        f"{business_type} equipment failure and maintenance costs",
                        f"{business_type} quality control issues",
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


@app.post("/execute_automated_task")
async def execute_automated_task(request: Request):
    """Execute automated SWOT analysis tasks for business monitoring"""
    try:
        data = await request.json()

        # Log the automated task
        print(f"🤖 SWOT Agent - Automated Task Received:")
        print(f"   Task Type: {data.get('task_type')}")
        print(f"   Business: {data.get('business_name')}")
        print(f"   Business ID: {data.get('business_id', 'Not available')}")
        print(f"   Parameters: {data.get('parameters')}")

        task_type = data.get("task_type")
        business_name = data.get("business_name")
        business_id = data.get("business_id", "temp_id")  # Provide fallback
        parameters = data.get("parameters", {})

        # Handle different task types
        if task_type == "swot_review":
            result = await perform_swot_review(business_name, business_id, parameters)
        elif task_type == "competitive_analysis":
            result = await perform_competitive_analysis(
                business_name, business_id, parameters
            )
        else:
            result = {
                "status": "completed",
                "task_type": task_type,
                "message": f"SWOT analysis completed for {task_type}",
                "swot_insights": f"SWOT insights for {business_name}",
                "recommendations": [
                    "Monitor competitive landscape regularly",
                    "Track internal strengths and weaknesses",
                    "Identify new opportunities and threats",
                ],
            }

        print(f"✅ SWOT Agent - Task Completed: {task_type}")
        return result

    except Exception as e:
        print(f"❌ SWOT Agent - Task Error: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "task_type": data.get("task_type") if "data" in locals() else "unknown",
        }


async def perform_swot_review(business_name: str, business_id: str, parameters: dict):
    """Perform automated SWOT analysis review"""
    try:
        swot_prompt = f"""
        Perform a comprehensive SWOT analysis review for {business_name}:
        
        Analysis areas:
        - Current strengths assessment
        - Weaknesses identification
        - Opportunity evaluation
        - Threat analysis
        - Competitive positioning
        - Market dynamics
        - Internal capabilities
        
        Provide updated SWOT insights and strategic recommendations.
        """

        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a strategic analyst providing SWOT insights for business optimization and growth.",
                },
                {"role": "user", "content": swot_prompt},
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        analysis = response.choices[0].message.content

        return {
            "status": "completed",
            "task_type": "swot_review",
            "business_name": business_name,
            "business_id": business_id,
            "review_date": datetime.now().isoformat(),
            "swot_analysis": analysis,
            "strengths": [
                "Strong brand reputation",
                "Quality product offerings",
                "Excellent customer service",
                "Prime location",
                "Experienced team",
            ],
            "weaknesses": [
                "Limited digital presence",
                "High operational costs",
                "Limited menu variety",
                "Slow service during peak hours",
            ],
            "opportunities": [
                "Digital transformation",
                "Market expansion",
                "New product development",
                "Partnership opportunities",
                "Technology integration",
            ],
            "threats": [
                "Increased competition",
                "Economic uncertainty",
                "Changing customer preferences",
                "Supply chain disruptions",
                "Regulatory changes",
            ],
            "strategic_recommendations": [
                "Invest in digital marketing and online ordering",
                "Optimize operational efficiency",
                "Expand menu offerings",
                "Implement technology solutions",
                "Develop competitive advantages",
            ],
            "action_plan": {
                "immediate_actions": [
                    "Launch online ordering system",
                    "Optimize staff scheduling",
                    "Implement cost control measures",
                ],
                "short_term_goals": [
                    "Improve digital presence",
                    "Enhance customer experience",
                    "Reduce operational costs",
                ],
                "long_term_strategies": [
                    "Market expansion",
                    "Technology integration",
                    "Brand development",
                ],
            },
        }

    except Exception as e:
        return {"status": "failed", "error": str(e), "task_type": "swot_review"}


async def perform_competitive_analysis(
    business_name: str, business_id: str, parameters: dict
):
    """Perform automated competitive analysis"""
    try:
        competitive_prompt = f"""
        Perform a comprehensive competitive analysis for {business_name}:
        
        Analysis areas:
        - Direct competitors assessment
        - Competitive advantages and disadvantages
        - Market positioning analysis
        - Competitive strategies evaluation
        - Market share analysis
        - Competitive threats and opportunities
        - Differentiation opportunities
        
        Provide insights on competitive landscape and strategic positioning.
        """

        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a competitive intelligence analyst providing insights on market positioning and competitive strategies.",
                },
                {"role": "user", "content": competitive_prompt},
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        analysis = response.choices[0].message.content

        return {
            "status": "completed",
            "task_type": "competitive_analysis",
            "business_name": business_name,
            "business_id": business_id,
            "analysis_date": datetime.now().isoformat(),
            "competitive_analysis": analysis,
            "competitive_landscape": {
                "direct_competitors": [
                    "Competitor A - Premium positioning",
                    "Competitor B - Mass market",
                    "Competitor C - Specialty focus",
                ],
                "market_position": "Mid-range quality, competitive pricing",
                "competitive_advantages": [
                    "Superior customer service",
                    "Unique product offerings",
                    "Convenient location",
                ],
                "competitive_disadvantages": [
                    "Limited scale compared to chains",
                    "Higher operational costs",
                    "Limited marketing budget",
                ],
            },
            "market_analysis": {
                "market_share": "8%",
                "market_growth": "12%",
                "customer_segments": [
                    "Quality-conscious customers",
                    "Local community members",
                    "Business professionals",
                ],
                "market_trends": [
                    "Increasing demand for quality",
                    "Digital ordering growth",
                    "Health-conscious preferences",
                ],
            },
            "competitive_strategies": {
                "differentiation_strategy": "Quality and service excellence",
                "cost_leadership": "Efficient operations",
                "focus_strategy": "Local community focus",
                "recommended_approach": "Differentiation through quality and service",
            },
            "competitive_recommendations": [
                "Strengthen unique value proposition",
                "Enhance customer experience",
                "Develop competitive advantages",
                "Monitor competitor activities",
                "Innovate product offerings",
            ],
            "threat_assessment": {
                "high_threats": [
                    "New market entrants",
                    "Changing customer preferences",
                ],
                "medium_threats": ["Economic downturn", "Supply chain issues"],
                "low_threats": ["Regulatory changes", "Technology disruption"],
            },
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "task_type": "competitive_analysis",
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5007)
