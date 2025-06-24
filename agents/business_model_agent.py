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
        location = business_data.get("location", "")
        competitors = business_data.get("competitors", [])
        growth_goals = business_data.get("growth_goals", [])

        # Create prompt for Business Model Canvas
        prompt = f"""
        As a business model expert, create a comprehensive Business Model Canvas for the following business:

        Business Name: {business_name}
        Location: {location}
        Competitors: {', '.join(competitors)}
        Growth Goals: {', '.join(growth_goals)}
        
        Strategic Context: {strategic_plan.get('competitive_positioning', {}).get('unique_value_proposition', '')}
        SWOT Analysis Available: {bool(swot_analysis)}

        Please create a detailed Business Model Canvas with all nine building blocks:

        1. KEY PARTNERS - Who are our key partners and suppliers?
        2. KEY ACTIVITIES - What key activities does our value proposition require?
        3. KEY RESOURCES - What key resources does our value proposition require?
        4. VALUE PROPOSITIONS - What value do we deliver to the customer?
        5. CUSTOMER RELATIONSHIPS - What type of relationship does each customer segment expect?
        6. CHANNELS - Through which channels do our customer segments want to be reached?
        7. CUSTOMER SEGMENTS - For whom are we creating value?
        8. COST STRUCTURE - What are the most important costs inherent in our business model?
        9. REVENUE STREAMS - For what value are our customers really willing to pay?

        Focus on a coffee shop business in Thailand and provide specific, actionable details for each building block.
        """

        try:
            # Call OpenAI for Business Model Canvas
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert business model consultant specializing in Business Model Canvas development for small businesses, particularly in the food and beverage industry in Thailand.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2000,
                temperature=0.7,
            )

            canvas_analysis_text = response.choices[0].message.content

            # Structure the Business Model Canvas
            business_model_canvas = {
                "business_name": business_name,
                "canvas_timestamp": datetime.now().isoformat(),
                "key_partners": {
                    "suppliers": [
                        {
                            "partner": "Coffee Bean Suppliers",
                            "type": "Strategic Supplier",
                            "value": "Quality coffee beans and consistent supply",
                            "relationship": "Long-term contracts with volume discounts",
                        },
                        {
                            "partner": "Equipment Suppliers",
                            "type": "Service Provider",
                            "value": "Coffee machines, grinders, and maintenance",
                            "relationship": "Service contracts and training support",
                        },
                        {
                            "partner": "Local Food Suppliers",
                            "type": "Local Partner",
                            "value": "Fresh pastries, sandwiches, and ingredients",
                            "relationship": "Daily supply with quality assurance",
                        },
                    ],
                    "strategic_partners": [
                        {
                            "partner": "Co-working Spaces",
                            "type": "Business Partner",
                            "value": "Regular corporate customers and events",
                            "relationship": "Exclusive discounts and delivery services",
                        },
                        {
                            "partner": "Local Artists and Musicians",
                            "type": "Creative Partner",
                            "value": "Unique atmosphere and cultural events",
                            "relationship": "Revenue sharing and exposure opportunities",
                        },
                        {
                            "partner": "Tourism Agencies",
                            "type": "Marketing Partner",
                            "value": "Tourist customers and promotional opportunities",
                            "relationship": "Commission-based referrals and packages",
                        },
                    ],
                    "technology_partners": [
                        {
                            "partner": "POS System Providers",
                            "type": "Technology Partner",
                            "value": "Point-of-sale and inventory management",
                            "relationship": "Subscription-based service with support",
                        },
                        {
                            "partner": "Delivery Platforms",
                            "type": "Service Partner",
                            "value": "Online ordering and delivery services",
                            "relationship": "Commission-based revenue sharing",
                        },
                    ],
                },
                "key_activities": {
                    "core_activities": [
                        {
                            "activity": "Coffee Preparation and Quality Control",
                            "description": "Expert coffee brewing and quality assurance",
                            "importance": "Critical - Core value proposition",
                            "resources_required": "Skilled baristas, quality equipment",
                        },
                        {
                            "activity": "Customer Service and Relationship Building",
                            "description": "Personalized service and community engagement",
                            "importance": "High - Competitive differentiation",
                            "resources_required": "Trained staff, CRM system",
                        },
                        {
                            "activity": "Inventory and Supply Chain Management",
                            "description": "Efficient procurement and stock management",
                            "importance": "High - Cost control and quality",
                            "resources_required": "Supplier relationships, inventory system",
                        },
                    ],
                    "supporting_activities": [
                        {
                            "activity": "Marketing and Brand Development",
                            "description": "Digital marketing, social media, and brand building",
                            "importance": "Medium - Customer acquisition",
                            "resources_required": "Marketing expertise, content creation",
                        },
                        {
                            "activity": "Staff Training and Development",
                            "description": "Continuous training and skill development",
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
                            "resource": "Prime Location",
                            "type": "Physical",
                            "description": "High-traffic location in Bangkok",
                            "value": "Customer accessibility and visibility",
                        },
                        {
                            "resource": "Coffee Equipment",
                            "type": "Physical",
                            "description": "Professional coffee machines and tools",
                            "value": "Quality coffee production capability",
                        },
                        {
                            "resource": "Store Interior and Atmosphere",
                            "type": "Physical",
                            "description": "Welcoming and comfortable space",
                            "value": "Customer experience and retention",
                        },
                    ],
                    "human_resources": [
                        {
                            "resource": "Skilled Baristas",
                            "type": "Human",
                            "description": "Expert coffee preparation and service",
                            "value": "Quality assurance and customer satisfaction",
                        },
                        {
                            "resource": "Management Team",
                            "type": "Human",
                            "description": "Business operations and strategy",
                            "value": "Operational efficiency and growth",
                        },
                        {
                            "resource": "Marketing Specialist",
                            "type": "Human",
                            "description": "Digital marketing and brand development",
                            "value": "Customer acquisition and brand awareness",
                        },
                    ],
                    "intellectual_resources": [
                        {
                            "resource": "Coffee Knowledge and Expertise",
                            "type": "Intellectual",
                            "description": "Deep understanding of coffee and brewing",
                            "value": "Quality differentiation and customer education",
                        },
                        {
                            "resource": "Local Market Knowledge",
                            "type": "Intellectual",
                            "description": "Understanding of Thai coffee culture",
                            "value": "Market positioning and customer insights",
                        },
                        {
                            "resource": "Business Processes and Systems",
                            "type": "Intellectual",
                            "description": "Standardized operations and quality control",
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5008)
