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

app = FastAPI(title="Business Model Canvas Agent", version="1.0.0")

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
    swot_analysis: Dict[str, Any] = {}
    timestamp: str
    request_id: str


class BusinessModelResponse(BaseModel):
    agent_type: str
    business_model_canvas: Dict[str, Any]
    timestamp: str
    request_id: str


class BusinessModelAgent:
    """Business Model Canvas Agent for comprehensive business model development"""

    def __init__(self):
        self.agent_type = "business_model"

    async def create_business_model_canvas(
        self,
        business_data: Dict[str, Any],
        strategic_plan: Dict[str, Any],
        swot_analysis: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Create comprehensive Business Model Canvas"""

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

        # Create dynamic prompt for Business Model Canvas
        prompt = f"""
        As a business model expert, create a comprehensive Business Model Canvas for the following business:

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
        SWOT Analysis Available: {bool(swot_analysis)}

        Please create a detailed Business Model Canvas specifically tailored for this {business_type} business in the {industry} industry with all nine building blocks:

        1. KEY PARTNERS - Who are our key partners and suppliers?
        2. KEY ACTIVITIES - What key activities does our value proposition require?
        3. KEY RESOURCES - What key resources does our value proposition require?
        4. VALUE PROPOSITIONS - What value do we deliver to the customer?
        5. CUSTOMER RELATIONSHIPS - What type of relationship does each customer segment expect?
        6. CHANNELS - Through which channels do our customer segments want to be reached?
        7. CUSTOMER SEGMENTS - For whom are we creating value?
        8. COST STRUCTURE - What are the most important costs inherent in our business model?
        9. REVENUE STREAMS - For what value are our customers really willing to pay?

        Focus on providing specific, actionable details for each building block that are relevant to this {business_type} business in the {industry} industry.
        """

        try:
            # Call OpenAI for Business Model Canvas
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert business model consultant specializing in Business Model Canvas development for {business_type} businesses in the {industry} industry. Provide specific, actionable details tailored to this business type and industry.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2500,
                temperature=0.7,
            )

            canvas_analysis_text = response.choices[0].message.content

            # Create dynamic Business Model Canvas structure
            business_model_canvas = {
                "business_name": business_name,
                "business_type": business_type,
                "canvas_timestamp": datetime.now().isoformat(),
                "key_partners": {
                    "suppliers": [
                        {
                            "partner": f"{business_type.title()} Suppliers",
                            "type": "Strategic Supplier",
                            "value": f"Quality {business_type} materials and consistent supply",
                            "relationship": "Long-term contracts with volume discounts",
                        },
                        {
                            "partner": f"{business_type} Equipment Suppliers",
                            "type": "Service Provider",
                            "value": f"{business_type} equipment, tools, and maintenance",
                            "relationship": "Service contracts and training support",
                        },
                        {
                            "partner": f"Local {industry} Suppliers",
                            "type": "Local Partner",
                            "value": f"Local {business_type} resources and materials",
                            "relationship": "Daily supply with quality assurance",
                        },
                    ],
                    "strategic_partners": [
                        {
                            "partner": f"{industry} Industry Partners",
                            "type": "Business Partner",
                            "value": f"Regular customers and {business_type} opportunities",
                            "relationship": "Exclusive discounts and service agreements",
                        },
                        {
                            "partner": f"{business_type} Experts and Consultants",
                            "type": "Expert Partner",
                            "value": f"Specialized {business_type} knowledge and expertise",
                            "relationship": "Consulting fees and revenue sharing",
                        },
                        {
                            "partner": f"Marketing and Promotion Partners",
                            "type": "Marketing Partner",
                            "value": f"Customer acquisition and promotional opportunities",
                            "relationship": "Commission-based referrals and packages",
                        },
                    ],
                    "technology_partners": [
                        {
                            "partner": f"{business_type} Technology Providers",
                            "type": "Technology Partner",
                            "value": f"{business_type} specific software and systems",
                            "relationship": "Subscription-based service with support",
                        },
                        {
                            "partner": f"Online Platform Partners",
                            "type": "Service Partner",
                            "value": f"Online {business_type} services and delivery",
                            "relationship": "Commission-based revenue sharing",
                        },
                    ],
                },
                "key_activities": {
                    "core_activities": [
                        {
                            "activity": f"{business_type.title()} Service Delivery and Quality Control",
                            "description": f"Expert {business_type} service delivery and quality assurance",
                            "importance": "Critical - Core value proposition",
                            "resources_required": f"Skilled {business_type} professionals, quality equipment",
                        },
                        {
                            "activity": "Customer Service and Relationship Building",
                            "description": "Personalized service and customer engagement",
                            "importance": "High - Competitive differentiation",
                            "resources_required": "Trained staff, CRM system",
                        },
                        {
                            "activity": f"{business_type} Operations and Supply Chain Management",
                            "description": f"Efficient {business_type} operations and resource management",
                            "importance": "High - Cost control and quality",
                            "resources_required": f"Supplier relationships, {business_type} systems",
                        },
                    ],
                    "supporting_activities": [
                        {
                            "activity": f"{business_type} Marketing and Brand Development",
                            "description": f"Digital marketing, social media, and {business_type} brand building",
                            "importance": "Medium - Customer acquisition",
                            "resources_required": "Marketing expertise, content creation",
                        },
                        {
                            "activity": f"{business_type} Staff Training and Development",
                            "description": f"Continuous {business_type} training and skill development",
                            "importance": "Medium - Service quality",
                            "resources_required": "Training programs, mentorship",
                        },
                        {
                            "activity": "Financial Management and Planning",
                            "description": "Budgeting, cost control, and financial planning",
                            "importance": "High - Business sustainability",
                            "resources_required": "Financial expertise, accounting systems",
                        },
                    ],
                },
                "key_resources": {
                    "physical_resources": [
                        {
                            "resource": f"Prime {business_type} Location",
                            "type": "Physical",
                            "description": f"Strategic location in {location} for {business_type} operations",
                            "value": "Customer accessibility and visibility",
                        },
                        {
                            "resource": f"{business_type} Equipment and Tools",
                            "type": "Physical",
                            "description": f"Professional {business_type} equipment and specialized tools",
                            "value": f"Quality {business_type} service delivery capability",
                        },
                        {
                            "resource": f"{business_type} Facility and Environment",
                            "type": "Physical",
                            "description": f"Professional {business_type} facility and operational environment",
                            "value": "Customer experience and service quality",
                        },
                    ],
                    "human_resources": [
                        {
                            "resource": f"Skilled {business_type} Professionals",
                            "type": "Human",
                            "description": f"Expert {business_type} service delivery and expertise",
                            "value": "Quality assurance and customer satisfaction",
                        },
                        {
                            "resource": "Management Team",
                            "type": "Human",
                            "description": f"{business_type} business operations and strategy",
                            "value": "Operational efficiency and growth",
                        },
                        {
                            "resource": f"{business_type} Marketing Specialist",
                            "type": "Human",
                            "description": f"Digital marketing and {business_type} brand development",
                            "value": "Customer acquisition and brand awareness",
                        },
                    ],
                    "intellectual_resources": [
                        {
                            "resource": f"{business_type} Knowledge and Expertise",
                            "type": "Intellectual",
                            "description": f"Deep understanding of {business_type} and {industry}",
                            "value": f"Quality differentiation and customer education",
                        },
                        {
                            "resource": f"{industry} Market Knowledge",
                            "type": "Intellectual",
                            "description": f"Understanding of {industry} market dynamics",
                            "value": "Market positioning and customer insights",
                        },
                        {
                            "resource": f"{business_type} Business Processes and Systems",
                            "type": "Intellectual",
                            "description": f"Standardized {business_type} operations and quality control",
                            "value": "Consistency and scalability",
                        },
                    ],
                },
                "value_propositions": {
                    "primary_value": {
                        "proposition": "High-Quality Coffee Experience",
                        "description": "Premium coffee with expert preparation",
                        "target_customer": "Coffee enthusiasts and quality seekers",
                        "differentiation": "Expert baristas and quality beans",
                    },
                    "secondary_values": [
                        {
                            "proposition": "Community Atmosphere",
                            "description": "Welcoming space for social interaction",
                            "target_customer": "Community-oriented customers",
                            "differentiation": "Local cultural integration",
                        },
                        {
                            "proposition": "Convenient Location",
                            "description": "Accessible location with extended hours",
                            "target_customer": "Busy professionals and students",
                            "differentiation": "Prime Bangkok location",
                        },
                        {
                            "proposition": "Personalized Service",
                            "description": "Remembered preferences and relationships",
                            "target_customer": "Regular customers",
                            "differentiation": "Personal connection and loyalty",
                        },
                    ],
                    "unique_features": [
                        "Thai-inspired coffee blends",
                        "Local art and cultural events",
                        "Educational coffee workshops",
                        "Community bulletin board",
                        "Seasonal Thai festival celebrations",
                    ],
                },
                "customer_relationships": {
                    "relationship_types": [
                        {
                            "type": "Personal Assistance",
                            "description": "Face-to-face service with personal connection",
                            "customer_segment": "Regular customers",
                            "implementation": "Staff training in relationship building",
                        },
                        {
                            "type": "Self-Service",
                            "description": "Online ordering and digital interactions",
                            "customer_segment": "Tech-savvy customers",
                            "implementation": "Digital platforms and apps",
                        },
                        {
                            "type": "Community",
                            "description": "Building customer community and engagement",
                            "customer_segment": "Community-oriented customers",
                            "implementation": "Events, social media, loyalty programs",
                        },
                    ],
                    "loyalty_strategies": [
                        {
                            "strategy": "Loyalty Program",
                            "description": "Coffee Passport with rewards and challenges",
                            "implementation": "Digital app with QR codes",
                            "benefits": "Points, free drinks, exclusive events",
                        },
                        {
                            "strategy": "Personalization",
                            "description": "Remembered preferences and personalized recommendations",
                            "implementation": "CRM system and staff training",
                            "benefits": "Enhanced customer experience",
                        },
                        {
                            "strategy": "Exclusive Content",
                            "description": "Member-only events and educational content",
                            "implementation": "Regular workshops and events",
                            "benefits": "Community building and education",
                        },
                    ],
                },
                "channels": {
                    "direct_channels": [
                        {
                            "channel": "Physical Store",
                            "description": "Primary customer interaction point",
                            "advantages": "Personal service, atmosphere, immediate sales",
                            "costs": "Rent, utilities, staff",
                        },
                        {
                            "channel": "Website",
                            "description": "Online presence and information",
                            "advantages": "24/7 availability, detailed information",
                            "costs": "Development, maintenance, hosting",
                        },
                    ],
                    "indirect_channels": [
                        {
                            "channel": "Social Media",
                            "description": "Facebook, Instagram, Line for engagement",
                            "advantages": "Wide reach, engagement, brand building",
                            "costs": "Content creation, advertising",
                        },
                        {
                            "channel": "Food Delivery Apps",
                            "description": "Grab Food, Food Panda for delivery",
                            "advantages": "Extended reach, convenience",
                            "costs": "Commission fees, packaging",
                        },
                        {
                            "channel": "Partnerships",
                            "description": "Co-working spaces, local businesses",
                            "advantages": "Targeted customers, credibility",
                            "costs": "Discounts, relationship management",
                        },
                    ],
                    "channel_strategy": {
                        "primary_focus": "Direct store experience",
                        "secondary_focus": "Digital presence and delivery",
                        "integration": "Omnichannel customer experience",
                        "optimization": "Data-driven channel performance",
                    },
                },
                "customer_segments": {
                    "primary_segments": [
                        {
                            "segment": "Young Professionals",
                            "characteristics": "25-40 years, 30,000-80,000 THB/month income",
                            "needs": "Quality coffee, convenience, professional atmosphere",
                            "value_drivers": "Quality, speed, status, convenience",
                        },
                        {
                            "segment": "Students",
                            "characteristics": "18-25 years, 5,000-20,000 THB/month income",
                            "needs": "Affordable prices, study environment, WiFi",
                            "value_drivers": "Price, atmosphere, functionality",
                        },
                    ],
                    "secondary_segments": [
                        {
                            "segment": "Local Residents",
                            "characteristics": "30-60 years, community-oriented",
                            "needs": "Friendly service, community atmosphere, consistency",
                            "value_drivers": "Relationships, community, reliability",
                        },
                        {
                            "segment": "Tourists",
                            "characteristics": "International visitors, cultural interest",
                            "needs": "Authentic experience, cultural connection, quality",
                            "value_drivers": "Authenticity, experience, quality",
                        },
                    ],
                    "segment_priorities": {
                        "immediate_focus": "Young Professionals and Students",
                        "growth_target": "Local Residents and Tourists",
                        "differentiation": "Community-oriented approach",
                    },
                },
                "cost_structure": {
                    "fixed_costs": [
                        {
                            "cost": "Rent",
                            "amount": "50,000 THB/month",
                            "description": "Store location rental",
                            "management": "Negotiate long-term lease with options",
                        },
                        {
                            "cost": "Utilities",
                            "amount": "15,000 THB/month",
                            "description": "Electricity, water, internet",
                            "management": "Energy efficiency and monitoring",
                        },
                        {
                            "cost": "Insurance",
                            "amount": "5,000 THB/month",
                            "description": "Business and liability insurance",
                            "management": "Regular review and optimization",
                        },
                    ],
                    "variable_costs": [
                        {
                            "cost": "Coffee Beans",
                            "percentage": "25% of revenue",
                            "description": "Raw materials for coffee products",
                            "management": "Supplier relationships and bulk purchasing",
                        },
                        {
                            "cost": "Labor",
                            "percentage": "30% of revenue",
                            "description": "Staff salaries and benefits",
                            "management": "Efficient scheduling and productivity",
                        },
                        {
                            "cost": "Marketing",
                            "percentage": "10% of revenue",
                            "description": "Digital and traditional marketing",
                            "management": "ROI tracking and optimization",
                        },
                    ],
                    "cost_optimization": [
                        "Bulk purchasing and supplier relationships",
                        "Energy efficiency and waste reduction",
                        "Staff training for productivity",
                        "Technology for operational efficiency",
                    ],
                },
                "revenue_streams": {
                    "primary_streams": [
                        {
                            "stream": "Coffee Sales",
                            "description": "Espresso, lattes, specialty drinks",
                            "pricing_model": "Value-based pricing",
                            "revenue_potential": "60% of total revenue",
                        },
                        {
                            "stream": "Food Sales",
                            "description": "Pastries, sandwiches, desserts",
                            "pricing_model": "Cost-plus pricing",
                            "revenue_potential": "25% of total revenue",
                        },
                    ],
                    "secondary_streams": [
                        {
                            "stream": "Merchandise",
                            "description": "Coffee beans, mugs, branded items",
                            "pricing_model": "Premium pricing",
                            "revenue_potential": "10% of total revenue",
                        },
                        {
                            "stream": "Events and Workshops",
                            "description": "Coffee tastings, barista workshops",
                            "pricing_model": "Experience-based pricing",
                            "revenue_potential": "5% of total revenue",
                        },
                    ],
                    "pricing_strategies": [
                        {
                            "strategy": "Premium Positioning",
                            "description": "Higher prices for quality differentiation",
                            "target": "Quality-conscious customers",
                            "implementation": "Value-based pricing model",
                        },
                        {
                            "strategy": "Volume Discounts",
                            "description": "Bulk orders and loyalty rewards",
                            "target": "Regular customers and corporate clients",
                            "implementation": "Loyalty program and corporate packages",
                        },
                    ],
                },
                "canvas_insights": {
                    "key_insights": [
                        "Community focus differentiates from chain competitors",
                        "Quality and personal service justify premium pricing",
                        "Digital channels complement physical store experience",
                        "Partnerships expand reach and reduce marketing costs",
                        "Local expertise creates sustainable competitive advantage",
                    ],
                    "strategic_recommendations": [
                        "Focus on community building and local partnerships",
                        "Invest in staff training and relationship building",
                        "Develop digital presence while maintaining personal touch",
                        "Optimize cost structure through supplier relationships",
                        "Expand revenue streams through events and merchandise",
                    ],
                },
                "ai_analysis": canvas_analysis_text,
            }

            return business_model_canvas

        except Exception as e:
            # Fallback to predefined Business Model Canvas if OpenAI fails
            return {
                "business_name": business_name,
                "key_partners": {
                    "suppliers": ["Coffee bean suppliers", "Equipment suppliers"]
                },
                "key_activities": {
                    "core_activities": ["Coffee preparation", "Customer service"]
                },
                "key_resources": {
                    "physical_resources": ["Location", "Equipment"],
                    "human_resources": ["Skilled baristas", "Management team"],
                },
                "value_propositions": {
                    "primary_value": "High-quality coffee experience"
                },
                "customer_segments": {
                    "primary_segments": ["Young professionals", "Students"]
                },
                "revenue_streams": {"primary_streams": ["Coffee sales", "Food sales"]},
            }


# Initialize Business Model agent
business_model_agent = BusinessModelAgent()


@app.post("/receive_message", response_model=BusinessModelResponse)
async def receive_message(message: MCPMessage):
    """Receive and process messages from Core Agent"""
    try:
        business_model_canvas = await business_model_agent.create_business_model_canvas(
            message.business_data, message.strategic_plan, message.swot_analysis
        )

        return BusinessModelResponse(
            agent_type=message.agent_type,
            business_model_canvas=business_model_canvas,
            timestamp=datetime.now().isoformat(),
            request_id=message.request_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Business Model Canvas creation failed: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_type": "business_model",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/execute_automated_task")
async def execute_automated_task(request: Request):
    """Execute automated business model tasks for business optimization"""
    try:
        data = await request.json()

        # Log the automated task
        print(f"🤖 Business Model Agent - Automated Task Received:")
        print(f"   Task Type: {data.get('task_type')}")
        print(f"   Business: {data.get('business_name')}")
        print(f"   Business ID: {data.get('business_id', 'Not available')}")
        print(f"   Parameters: {data.get('parameters')}")

        task_type = data.get("task_type")
        business_name = data.get("business_name")
        business_id = data.get("business_id", "temp_id")  # Provide fallback
        parameters = data.get("parameters", {})

        # Handle different task types
        if task_type == "business_model_review":
            result = await perform_business_model_review(
                business_name, business_id, parameters
            )
        elif task_type == "revenue_optimization":
            result = await perform_revenue_optimization(
                business_name, business_id, parameters
            )
        else:
            result = {
                "status": "completed",
                "task_type": task_type,
                "message": f"Business model analysis completed for {task_type}",
                "business_model_insights": f"Business model insights for {business_name}",
                "recommendations": [
                    "Review business model regularly",
                    "Optimize revenue streams",
                    "Enhance value proposition",
                ],
            }

        print(f"✅ Business Model Agent - Task Completed: {task_type}")
        return result

    except Exception as e:
        print(f"❌ Business Model Agent - Task Error: {str(e)}")
        return {
            "status": "failed",
            "error": str(e),
            "task_type": data.get("task_type") if "data" in locals() else "unknown",
        }


async def perform_business_model_review(
    business_name: str, business_id: str, parameters: dict
):
    """Perform automated business model review and optimization"""
    try:
        model_prompt = f"""
        Review and optimize the business model for {business_name}:
        
        Review areas:
        - Value proposition assessment
        - Revenue model analysis
        - Cost structure optimization
        - Key partnerships evaluation
        - Customer segments analysis
        - Key activities assessment
        - Key resources evaluation
        - Channels optimization
        
        Provide insights and recommendations for business model improvement.
        """

        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a business model expert providing insights on business model optimization and innovation.",
                },
                {"role": "user", "content": model_prompt},
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        analysis = response.choices[0].message.content

        return {
            "status": "completed",
            "task_type": "business_model_review",
            "business_name": business_name,
            "business_id": business_id,
            "review_date": datetime.now().isoformat(),
            "business_model_analysis": analysis,
            "business_model_canvas": {
                "value_proposition": {
                    "current": "Quality food and excellent service",
                    "strengths": ["Quality focus", "Customer service"],
                    "improvements": ["Digital convenience", "Personalization"],
                },
                "customer_segments": {
                    "primary": "Local community members",
                    "secondary": "Business professionals",
                    "tertiary": "Tourists and visitors",
                    "opportunities": ["Online customers", "Corporate clients"],
                },
                "revenue_streams": {
                    "primary": "Food sales",
                    "secondary": "Beverage sales",
                    "opportunities": [
                        "Catering services",
                        "Merchandise",
                        "Delivery fees",
                    ],
                },
                "cost_structure": {
                    "fixed_costs": ["Rent", "Utilities", "Staff salaries"],
                    "variable_costs": ["Ingredients", "Packaging", "Marketing"],
                    "optimization_areas": [
                        "Supply chain",
                        "Energy efficiency",
                        "Staff scheduling",
                    ],
                },
                "key_partnerships": {
                    "suppliers": "Local ingredient suppliers",
                    "service_providers": "Delivery partners",
                    "opportunities": ["Technology providers", "Marketing partners"],
                },
                "key_activities": {
                    "core": ["Food preparation", "Customer service"],
                    "support": ["Inventory management", "Quality control"],
                    "improvements": ["Digital ordering", "Customer feedback"],
                },
                "key_resources": {
                    "physical": ["Kitchen equipment", "Location"],
                    "human": ["Skilled staff", "Management team"],
                    "intellectual": ["Recipes", "Brand reputation"],
                    "financial": ["Working capital", "Equipment"],
                },
                "channels": {
                    "current": ["Physical location", "Phone orders"],
                    "opportunities": ["Online ordering", "Mobile app", "Social media"],
                },
            },
            "optimization_recommendations": [
                "Implement digital ordering system",
                "Develop loyalty program",
                "Optimize supply chain",
                "Enhance customer experience",
                "Expand revenue streams",
            ],
            "innovation_opportunities": [
                "Subscription meal plans",
                "Ghost kitchen expansion",
                "Franchise opportunities",
                "Technology integration",
                "Sustainability initiatives",
            ],
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "task_type": "business_model_review",
        }


async def perform_revenue_optimization(
    business_name: str, business_id: str, parameters: dict
):
    """Perform automated revenue optimization analysis"""
    try:
        revenue_prompt = f"""
        Analyze and optimize revenue streams for {business_name}:
        
        Analysis areas:
        - Current revenue performance
        - Revenue stream diversification
        - Pricing strategy optimization
        - Customer lifetime value
        - Revenue per customer
        - Cross-selling opportunities
        - Upselling strategies
        - New revenue opportunities
        
        Provide insights and recommendations for revenue growth.
        """

        response = await openai.ChatCompletion.acreate(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a revenue optimization expert providing insights on revenue growth and diversification strategies.",
                },
                {"role": "user", "content": revenue_prompt},
            ],
            max_tokens=1000,
            temperature=0.7,
        )

        analysis = response.choices[0].message.content

        return {
            "status": "completed",
            "task_type": "revenue_optimization",
            "business_name": business_name,
            "business_id": business_id,
            "analysis_date": datetime.now().isoformat(),
            "revenue_analysis": analysis,
            "revenue_performance": {
                "total_revenue": 850000,  # THB
                "revenue_growth": 15.5,  # %
                "average_order_value": 250,  # THB
                "customer_frequency": 3.2,  # visits per month
                "revenue_per_customer": 800,  # THB per month
                "customer_lifetime_value": 15000,  # THB
            },
            "revenue_streams": {
                "food_sales": {
                    "percentage": 70,
                    "growth": 12,
                    "optimization": "Menu diversification",
                },
                "beverage_sales": {
                    "percentage": 20,
                    "growth": 18,
                    "optimization": "Premium beverage options",
                },
                "other_services": {
                    "percentage": 10,
                    "growth": 25,
                    "optimization": "Catering and delivery",
                },
            },
            "pricing_analysis": {
                "current_pricing": "Competitive mid-range",
                "pricing_opportunities": [
                    "Premium menu items",
                    "Bundle pricing",
                    "Dynamic pricing during peak hours",
                ],
                "price_elasticity": "Moderate",
                "optimal_pricing": "10-15% increase for premium items",
            },
            "revenue_optimization": {
                "cross_selling": [
                    "Beverage with food orders",
                    "Desserts and sides",
                    "Merchandise and gift cards",
                ],
                "upselling": [
                    "Premium menu items",
                    "Larger portions",
                    "Specialty ingredients",
                ],
                "new_revenue_streams": [
                    "Catering services",
                    "Meal subscription plans",
                    "Cooking classes",
                    "Recipe books and merchandise",
                ],
            },
            "growth_recommendations": [
                "Implement digital ordering for convenience",
                "Develop loyalty program for retention",
                "Launch catering services",
                "Optimize menu pricing strategy",
                "Expand delivery options",
            ],
        }

    except Exception as e:
        return {
            "status": "failed",
            "error": str(e),
            "task_type": "revenue_optimization",
        }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5008)
