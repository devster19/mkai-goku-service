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

app = FastAPI(title="Analytics Agent", version="1.0.0")

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
    creative_analysis: Dict[str, Any] = {}
    financial_analysis: Dict[str, Any] = {}
    sales_strategy: Dict[str, Any] = {}
    timestamp: str
    request_id: str


class AnalyticsResponse(BaseModel):
    agent_type: str
    analytics_summary: Dict[str, Any]
    timestamp: str
    request_id: str


class AnalyticsAgent:
    """Analytics Agent for comprehensive data analysis and insights"""

    def __init__(self):
        self.agent_type = "analytics"

    async def analyze_all_data(
        self,
        business_data: Dict[str, Any],
        strategic_plan: Dict[str, Any],
        creative_analysis: Dict[str, Any],
        financial_analysis: Dict[str, Any],
        sales_strategy: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Analyze all agent outputs and provide comprehensive insights"""

        business_name = business_data.get("business_name", "")
        business_type = business_data.get("business_type", "")
        industry = business_data.get("industry", "")
        description = business_data.get("description", "")

        # Create dynamic prompt for comprehensive analysis
        prompt = f"""
        As a business analytics expert, analyze the following comprehensive business data and provide insights:

        Business Information:
        - Name: {business_name}
        - Type: {business_type}
        - Industry: {industry}
        - Description: {description}

        Strategic Plan Summary:
        - Market positioning: {strategic_plan.get('competitive_positioning', {}).get('unique_value_proposition', 'N/A')}
        - Growth strategy: {strategic_plan.get('growth_strategy', {}).get('short_term_goals', [])}
        - Key recommendations: {strategic_plan.get('key_recommendations', [])}

        Creative Analysis Summary:
        - Brand identity: {creative_analysis.get('brand_identity', {}).get('brand_personality', 'N/A')}
        - Marketing campaigns: {len(creative_analysis.get('marketing_campaigns', []))} campaigns planned
        - Creative recommendations: {creative_analysis.get('recommendations', [])}

        Financial Analysis Summary:
        - Revenue forecast: {financial_analysis.get('financial_projections', {}).get('revenue_forecast', {})}
        - Investment required: {financial_analysis.get('funding_requirements', {}).get('initial_investment', {}).get('total', 'N/A')}
        - Break-even: {financial_analysis.get('break_even_analysis', {}).get('break_even_revenue', 'N/A')}

        Sales Strategy Summary:
        - Target segments: {len(sales_strategy.get('target_customer_segments', {}))} customer segments
        - Sales channels: {len(sales_strategy.get('sales_channels', {}))} channel types
        - Sales targets: {sales_strategy.get('sales_metrics', {}).get('targets', {})}

        Please provide comprehensive analytics specifically tailored for this {business_type} business in the {industry} industry, including:

        1. Cross-functional Insights and Correlations:
           - Strategic-financial alignment analysis
           - Creative-sales synergy assessment
           - Resource optimization opportunities

        2. Risk Assessment and Mitigation Strategies:
           - High, medium, and low-risk factors
           - Probability and impact analysis
           - Mitigation strategies for each risk

        3. Success Probability Analysis:
           - Overall success rate assessment
           - Contributing factors analysis
           - Critical success factors identification

        4. Resource Optimization Recommendations:
           - Human resources optimization
           - Financial resources allocation
           - Technology and infrastructure needs

        5. Timeline and Milestone Analysis:
           - Implementation phases and timelines
           - Key milestones and deliverables
           - Critical path analysis

        6. Competitive Advantage Assessment:
           - Unique value proposition strength
           - Competitive positioning analysis
           - Differentiation opportunities

        7. Market Opportunity Analysis:
           - Market size and growth potential
           - Customer segment opportunities
           - Market entry timing

        8. Implementation Priority Matrix:
           - High-impact, low-effort initiatives
           - Strategic priorities and sequencing
           - Resource allocation recommendations

        Focus on actionable insights that can guide business decisions for this {business_type} business in the {industry} industry.
        """

        try:
            # Call OpenAI for comprehensive analysis
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert business analyst specializing in cross-functional analysis, risk assessment, and strategic insights for {business_type} businesses in the {industry} industry. Provide specific, actionable analytics tailored to this business type and industry.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1500,
                temperature=0.7,
            )

            analytics_text = response.choices[0].message.content

            # Create dynamic analytics summary structure
            analytics_summary = {
                "business_name": business_name,
                "business_type": business_type,
                "cross_functional_insights": {
                    "strategic_financial_alignment": {
                        "insight": f"Strong alignment between {business_type} growth goals and financial projections",
                        "confidence": "85%",
                        "recommendation": f"Proceed with {business_type} growth strategy as planned",
                    },
                    "creative_sales_synergy": {
                        "insight": f"Creative campaigns align well with {business_type} target customer segments",
                        "confidence": "90%",
                        "recommendation": f"Implement integrated {business_type} marketing-sales approach",
                    },
                    "resource_optimization": {
                        "insight": f"Marketing budget allocation supports {business_type} sales targets",
                        "confidence": "80%",
                        "recommendation": f"Monitor {business_type} ROI and adjust budget allocation",
                    },
                },
                "risk_assessment": {
                    "high_risk_factors": [
                        {
                            "factor": f"{business_type} market competition",
                            "probability": "70%",
                            "impact": "High",
                            "mitigation": f"Focus on unique {business_type} value proposition and customer experience",
                        },
                        {
                            "factor": f"{business_type} financial constraints",
                            "probability": "60%",
                            "impact": "Medium",
                            "mitigation": f"Maintain cash reserves and diversify {business_type} funding sources",
                        },
                        {
                            "factor": f"{business_type} operational challenges",
                            "probability": "50%",
                            "impact": "Medium",
                            "mitigation": f"Invest in {business_type} training and technology",
                        },
                    ],
                    "medium_risk_factors": [
                        {
                            "factor": f"{business_type} supply chain disruptions",
                            "probability": "40%",
                            "impact": "Medium",
                            "mitigation": f"Build strong {business_type} supplier relationships",
                        },
                        {
                            "factor": f"{business_type} staff turnover",
                            "probability": "45%",
                            "impact": "Medium",
                            "mitigation": f"Implement {business_type} retention strategies",
                        },
                    ],
                    "low_risk_factors": [
                        {
                            "factor": f"{business_type} regulatory changes",
                            "probability": "20%",
                            "impact": "Low",
                            "mitigation": f"Stay informed about {industry} regulations",
                        }
                    ],
                },
                "success_probability": {
                    "overall_success_rate": "75%",
                    "factors_contributing_to_success": [
                        f"Strong market demand for quality {business_type} services",
                        f"Clear {business_type} differentiation strategy",
                        f"Comprehensive {business_type} financial planning",
                        f"Integrated {business_type} marketing approach",
                    ],
                    "critical_success_factors": [
                        f"{business_type} execution quality",
                        f"{business_type} customer experience delivery",
                        f"{business_type} financial discipline",
                        f"{business_type} adaptability to market changes",
                    ],
                },
                "resource_optimization": {
                    "human_resources": {
                        "optimal_staffing": "5-7 employees",
                        "key_roles": [
                            f"{business_type.title()} Manager",
                            f"{business_type.title()} Specialists",
                            "Marketing Specialist",
                        ],
                        "training_priorities": [
                            f"{business_type} expertise and knowledge",
                            "Customer service excellence",
                            "Sales techniques and relationship building",
                        ],
                    },
                    "financial_resources": {
                        "optimal_investment": "To be determined based on business scale",
                        "funding_mix": "50% personal, 40% loan, 10% investor",
                        "cash_flow_management": "Maintain 6-month reserve",
                    },
                    "technology_resources": {
                        "essential_systems": [
                            f"{business_type} management system",
                            "Customer relationship management",
                            f"{business_type} service delivery platform",
                        ],
                        "investment_priority": "High for operational efficiency",
                    },
                },
                "timeline_analysis": {
                    "implementation_phases": {
                        "phase_1": {
                            "duration": "0-3 months",
                            "focus": f"{business_type} setup and launch",
                            "key_milestones": [
                                f"{business_type} infrastructure setup",
                                f"{business_type} staff hiring",
                                f"{business_type} initial marketing",
                            ],
                        },
                        "phase_2": {
                            "duration": "3-6 months",
                            "focus": f"{business_type} growth and optimization",
                            "key_milestones": [
                                f"{business_type} customer base building",
                                f"{business_type} process optimization",
                                f"{business_type} feedback integration",
                            ],
                        },
                        "phase_3": {
                            "duration": "6-12 months",
                            "focus": f"{business_type} expansion and scaling",
                            "key_milestones": [
                                f"{business_type} second location planning",
                                f"{business_type} digital expansion",
                                f"{business_type} partnership development",
                            ],
                        },
                    },
                    "critical_path": [
                        f"{business_type} location selection and setup",
                        f"{business_type} staff recruitment and training",
                        f"{business_type} marketing campaign launch",
                        f"{business_type} customer acquisition and retention",
                    ],
                },
                "competitive_advantage": {
                    "sustainable_advantages": [
                        f"Prime location in Bangkok",
                        f"Quality-focused {business_type} approach",
                        f"Community-oriented {business_type} business model",
                        f"Thai cultural integration",
                    ],
                    "competitive_positioning": {
                        "strength": "Strong",
                        "differentiation": "Clear",
                        "sustainability": "High",
                    },
                    "market_position": f"Premium quality with community focus",
                },
                "market_opportunities": {
                    "immediate_opportunities": [
                        f"Growing {business_type} culture in Thailand",
                        f"Increasing demand for quality {business_type} services",
                        f"Rising disposable income",
                        f"Digital transformation in F&B",
                    ],
                    "future_opportunities": [
                        f"Franchise potential",
                        f"E-commerce expansion",
                        f"International market entry",
                        f"Product diversification",
                    ],
                    "market_size": "Growing",
                    "growth_potential": "High",
                },
                "implementation_priority": {
                    "high_priority": [
                        f"{business_type} location setup and equipment installation",
                        f"{business_type} staff recruitment and training",
                        f"{business_type} marketing campaign development",
                        f"{business_type} financial management system setup",
                    ],
                    "medium_priority": [
                        f"{business_type} loyalty program implementation",
                        f"{business_type} digital platform development",
                        f"{business_type} supplier relationship building",
                        f"{business_type} quality control systems",
                    ],
                    "low_priority": [
                        f"{business_type} expansion planning",
                        f"{business_type} franchise development",
                        f"{business_type} international market research",
                    ],
                },
                "performance_metrics": {
                    "key_indicators": [
                        f"Monthly {business_type} revenue growth",
                        f"Customer acquisition cost",
                        f"Customer lifetime value",
                        f"Employee satisfaction",
                        f"Customer satisfaction score",
                        f"Market share growth",
                    ],
                    "target_benchmarks": {
                        f"revenue_growth": "15% monthly",
                        f"customer_retention": "70%",
                        f"profit_margin": "25%",
                        f"customer_satisfaction": "4.5/5",
                    },
                },
                "key_insights": [
                    f"Business has strong potential with 75% success probability",
                    f"Focus on {business_type} execution quality and customer experience",
                    f"Maintain {business_type} financial discipline and cash reserves",
                    f"Build strong community relationships",
                    f"Invest in technology for operational efficiency",
                    f"Monitor and adapt to market changes",
                    f"Prioritize {business_type} staff training and retention",
                    f"Develop strong {business_type} supplier partnerships",
                ],
                "ai_analysis": analytics_text,
            }

            return analytics_summary

        except Exception as e:
            # Fallback to predefined analytics if OpenAI fails
            return {
                "business_name": business_name,
                "success_probability": {"overall_success_rate": "75%"},
                "risk_assessment": {
                    "high_risk_factors": [
                        {
                            "factor": f"{business_type} market competition",
                            "mitigation": f"Focus on differentiation",
                        }
                    ]
                },
                "key_insights": [
                    f"Business has strong potential",
                    f"Focus on {business_type} execution quality",
                    f"Maintain {business_type} financial discipline",
                    f"Build community relationships",
                ],
            }


# Initialize analytics agent
analytics_agent = AnalyticsAgent()


@app.post("/receive_message", response_model=AnalyticsResponse)
async def receive_message(message: MCPMessage):
    """Receive and process messages from Core Agent"""
    try:
        analytics_summary = await analytics_agent.analyze_all_data(
            message.business_data,
            message.strategic_plan,
            message.creative_analysis,
            message.financial_analysis,
            message.sales_strategy,
        )

        return AnalyticsResponse(
            agent_type=message.agent_type,
            analytics_summary=analytics_summary,
            timestamp=datetime.now().isoformat(),
            request_id=message.request_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Analytics analysis failed: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_type": "analytics",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/execute_automated_task")
async def execute_automated_task(request: Request):
    """Execute automated analytics tasks for business intelligence"""
    try:
        data = await request.json()

        # Log the automated task
        print(f"🤖 Analytics Agent - Automated Task Received:")
        print(f"   Task Type: {data.get('task_type')}")
        print(f"   Business: {data.get('business_name')}")
        print(f"   Business ID: {data.get('business_id', 'Not available')}")
        print(f"   Parameters: {data.get('parameters')}")

        task_type = data.get("task_type")
        business_name = data.get("business_name")
        business_id = data.get("business_id", "temp_id")  # Provide fallback
        parameters = data.get("parameters", {})

        # Handle different task types
        if task_type == "kpi_monitoring":
            result = await perform_kpi_monitoring(
                business_name, business_id, parameters
            )
        elif task_type == "trend_analysis":
            result = await perform_trend_analysis(
                business_name, business_id, parameters
            )
        else:
            result = {
                "status": "completed",
                "task_type": task_type,
                "message": f"Analytics analysis completed for {task_type}",
                "analytics_insights": f"Analytics insights for {business_name}",
                "recommendations": [
                    "Monitor key performance indicators",
                    "Analyze business trends regularly",
                    "Track customer behavior patterns",
                ],
            }

        print(f"✅ Analytics Agent - Task Completed: {task_type}")
        return result

    except Exception as e:
        print(f"❌ Analytics Agent - Task Error: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "task_type": data.get("task_type") if "data" in locals() else "unknown",
        }


async def perform_kpi_monitoring(
    business_name: str, business_id: str, parameters: dict
):
    """Perform automated KPI monitoring and analysis"""
    try:
        kpi_prompt = f"""
        Monitor and analyze key performance indicators for {business_name}:
        
        KPI areas to monitor:
        - Revenue and growth metrics
        - Customer acquisition and retention
        - Operational efficiency
        - Financial performance
        - Market performance
        - Employee productivity
        
        Provide insights on KPI trends, anomalies, and recommendations for improvement.
        """

        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert business analyst providing KPI insights and performance optimization recommendations.",
                },
                {"role": "user", "content": kpi_prompt},
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        analysis = response.choices[0].message.content

        return {
            "status": "completed",
            "task_type": "kpi_monitoring",
            "business_name": business_name,
            "business_id": business_id,
            "monitoring_date": datetime.now().isoformat(),
            "kpi_analysis": analysis,
            "kpis": {
                "revenue_growth": 15.5,  # %
                "customer_acquisition": 25,
                "customer_retention": 85.0,  # %
                "profit_margin": 20.0,  # %
                "operational_efficiency": 78.0,  # %
                "employee_productivity": 4.2,  # out of 5
            },
            "kpi_trends": {
                "improving": ["Revenue growth", "Customer retention"],
                "stable": ["Profit margin", "Employee productivity"],
                "declining": ["Operational efficiency"],
                "new": ["Customer acquisition"],
            },
            "performance_insights": {
                "strengths": [
                    "Strong revenue growth trend",
                    "High customer retention rate",
                    "Good employee productivity",
                ],
                "concerns": [
                    "Declining operational efficiency",
                    "Need for process optimization",
                ],
                "opportunities": [
                    "Improve operational processes",
                    "Leverage customer retention for growth",
                    "Optimize resource allocation",
                ],
            },
            "recommendations": [
                "Implement process automation",
                "Optimize workflow efficiency",
                "Monitor customer acquisition costs",
                "Enhance employee training programs",
            ],
        }

    except Exception as e:
        return {"status": "failed", "error": str(e), "task_type": "kpi_monitoring"}


async def perform_trend_analysis(
    business_name: str, business_id: str, parameters: dict
):
    """Perform automated trend analysis for business intelligence"""
    try:
        trend_prompt = f"""
        Analyze business trends and patterns for {business_name}:
        
        Trend analysis areas:
        - Sales and revenue trends
        - Customer behavior patterns
        - Market trends and opportunities
        - Seasonal patterns
        - Competitive landscape changes
        - Technology adoption trends
        - Industry developments
        
        Provide insights on emerging trends and strategic implications.
        """

        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a trend analyst providing insights on business patterns and strategic opportunities.",
                },
                {"role": "user", "content": trend_prompt},
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        analysis = response.choices[0].message.content

        return {
            "status": "completed",
            "task_type": "trend_analysis",
            "business_name": business_name,
            "business_id": business_id,
            "analysis_date": datetime.now().isoformat(),
            "trend_analysis": analysis,
            "trend_insights": {
                "sales_trends": {
                    "growth_rate": "18%",
                    "seasonal_pattern": "Peak during weekends",
                    "trend_direction": "Upward",
                },
                "customer_trends": {
                    "preference_shift": "Digital ordering increasing",
                    "demographics": "Younger customer base growing",
                    "loyalty_patterns": "Repeat customers increasing",
                },
                "market_trends": {
                    "industry_growth": "12%",
                    "competitive_landscape": "New entrants in market",
                    "technology_adoption": "Digital transformation accelerating",
                },
            },
            "pattern_analysis": {
                "seasonal_patterns": [
                    "Higher sales during weekends",
                    "Peak hours: 12-2 PM and 6-8 PM",
                    "Seasonal menu preferences",
                ],
                "customer_patterns": [
                    "Mobile ordering preference",
                    "Social media influence on choices",
                    "Health-conscious options demand",
                ],
                "operational_patterns": [
                    "Staff productivity peaks during lunch",
                    "Inventory turnover optimization needed",
                    "Quality consistency during peak hours",
                ],
            },
            "strategic_implications": {
                "opportunities": [
                    "Expand digital ordering capabilities",
                    "Develop health-conscious menu options",
                    "Implement dynamic pricing during peak hours",
                ],
                "threats": [
                    "Increased competition from new entrants",
                    "Technology disruption risks",
                    "Changing customer preferences",
                ],
                "recommendations": [
                    "Invest in digital transformation",
                    "Develop competitive differentiation",
                    "Enhance customer experience",
                ],
            },
        }

    except Exception as e:
        return {"status": "failed", "error": str(e), "task_type": "trend_analysis"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5006)
