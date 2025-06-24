from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import openai
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Sales Agent", version="1.0.0")

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


class MCPMessage(BaseModel):
    agent_type: str
    business_data: Dict[str, Any]
    strategic_plan: Dict[str, Any] = {}
    timestamp: str
    request_id: str


class SalesResponse(BaseModel):
    agent_type: str
    sales_strategy: Dict[str, Any]
    timestamp: str
    request_id: str


class SalesAgent:
    """Sales Agent for sales strategy and customer acquisition"""

    def __init__(self):
        self.agent_type = "sales"

    async def analyze_sales_strategy(
        self, business_data: Dict[str, Any], strategic_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze sales strategy and customer acquisition"""

        business_name = business_data.get("business_name", "")
        location = business_data.get("location", "")
        competitors = business_data.get("competitors", [])
        growth_goals = business_data.get("growth_goals", [])

        # Create prompt for sales analysis
        prompt = f"""
        As a sales and customer acquisition expert, analyze the following business and provide sales strategy recommendations:

        Business Name: {business_name}
        Location: {location}
        Competitors: {', '.join(competitors)}
        Growth Goals: {', '.join(growth_goals)}
        
        Strategic Plan Context: {strategic_plan.get('competitive_positioning', {}).get('unique_value_proposition', '')}

        Please provide sales analysis including:
        1. Target customer segments and personas
        2. Sales channels and distribution strategy
        3. Customer acquisition strategies
        4. Sales process and pipeline
        5. Customer retention strategies
        6. Sales team structure and training
        7. Sales metrics and KPIs
        8. Partnership and collaboration opportunities

        Focus on practical sales strategies for a coffee shop business in Thailand.
        """

        try:
            # Call OpenAI for sales analysis
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert sales consultant specializing in customer acquisition, retention, and sales strategy for the food and beverage industry in Thailand.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1200,
                temperature=0.7,
            )

            sales_analysis_text = response.choices[0].message.content

            # Structure the sales analysis
            sales_strategy = {
                "business_name": business_name,
                "target_customer_segments": {
                    "primary_segment": {
                        "name": "Young Professionals",
                        "age_range": "25-40",
                        "income": "30,000-80,000 THB/month",
                        "characteristics": [
                            "Coffee enthusiasts",
                            "Value quality and convenience",
                            "Active on social media",
                            "Willing to pay premium for quality",
                        ],
                        "needs": [
                            "High-quality coffee",
                            "Convenient location",
                            "Professional atmosphere",
                            "Fast service",
                        ],
                    },
                    "secondary_segment": {
                        "name": "Students",
                        "age_range": "18-25",
                        "income": "5,000-20,000 THB/month",
                        "characteristics": [
                            "Budget-conscious",
                            "Social media active",
                            "Study/work in cafes",
                            "Value atmosphere and WiFi",
                        ],
                        "needs": [
                            "Affordable prices",
                            "Study-friendly environment",
                            "Free WiFi",
                            "Group seating",
                        ],
                    },
                    "tertiary_segment": {
                        "name": "Local Residents",
                        "age_range": "30-60",
                        "income": "20,000-100,000 THB/month",
                        "characteristics": [
                            "Community-oriented",
                            "Loyal customers",
                            "Word-of-mouth advocates",
                            "Value relationships",
                        ],
                        "needs": [
                            "Friendly service",
                            "Community atmosphere",
                            "Consistent quality",
                            "Local connection",
                        ],
                    },
                },
                "sales_channels": {
                    "direct_sales": {
                        "in-store": "Primary channel for immediate revenue",
                        "online_ordering": "Convenience for customers",
                        "delivery": "Expand reach and convenience",
                    },
                    "indirect_sales": {
                        "corporate_orders": "Bulk orders for offices",
                        "events_catering": "Weddings, corporate events",
                        "wholesale": "Supply to other businesses",
                    },
                    "digital_channels": {
                        "social_media": "Instagram, Facebook, Line",
                        "food_delivery_apps": "Grab Food, Food Panda",
                        "website": "Online ordering and information",
                    },
                },
                "customer_acquisition_strategies": {
                    "digital_marketing": [
                        {
                            "strategy": "Social media advertising",
                            "platforms": ["Facebook", "Instagram", "Line"],
                            "targeting": "Local audience, coffee enthusiasts",
                            "budget": "15,000 THB/month",
                        },
                        {
                            "strategy": "Google My Business optimization",
                            "focus": "Local SEO and reviews",
                            "budget": "5,000 THB/month",
                        },
                        {
                            "strategy": "Influencer partnerships",
                            "approach": "Local food bloggers and coffee enthusiasts",
                            "budget": "20,000 THB/month",
                        },
                    ],
                    "offline_marketing": [
                        {
                            "strategy": "Local partnerships",
                            "partners": ["Nearby offices", "Gyms", "Co-working spaces"],
                            "approach": "Referral programs and discounts",
                        },
                        {
                            "strategy": "Community events",
                            "events": ["Coffee tastings", "Local markets", "Festivals"],
                            "approach": "Brand visibility and sampling",
                        },
                        {
                            "strategy": "Print advertising",
                            "materials": [
                                "Flyers",
                                "Local magazines",
                                "Community boards",
                            ],
                            "budget": "10,000 THB/month",
                        },
                    ],
                },
                "sales_process": {
                    "customer_journey": {
                        "awareness": "Social media, local advertising, word-of-mouth",
                        "consideration": "Online reviews, website, social media content",
                        "purchase": "In-store visit, online ordering, delivery",
                        "retention": "Loyalty program, personalized service, follow-up",
                    },
                    "sales_techniques": [
                        "Product knowledge training for staff",
                        "Upselling and cross-selling techniques",
                        "Customer relationship management",
                        "Feedback collection and response",
                    ],
                },
                "customer_retention": {
                    "loyalty_program": {
                        "name": "Coffee Passport",
                        "features": [
                            "Points for every purchase",
                            "Free drink after 10 purchases",
                            "Birthday rewards",
                            "Exclusive member events",
                        ],
                        "technology": "Digital app with QR codes",
                    },
                    "relationship_building": [
                        "Remember customer names and preferences",
                        "Personalized recommendations",
                        "Regular communication via Line",
                        "Exclusive member content",
                    ],
                    "feedback_management": [
                        "Regular customer surveys",
                        "Social media monitoring",
                        "Review response strategy",
                        "Continuous improvement based on feedback",
                    ],
                },
                "sales_team": {
                    "structure": {
                        "manager": "1 full-time sales manager",
                        "baristas": "3-5 part-time baristas with sales training",
                        "marketing_specialist": "1 part-time digital marketing specialist",
                    },
                    "training_program": [
                        "Product knowledge and coffee expertise",
                        "Customer service excellence",
                        "Sales techniques and upselling",
                        "Technology and POS systems",
                        "Thai and English language skills",
                    ],
                    "compensation": {
                        "base_salary": "Competitive with market rates",
                        "performance_bonus": "Based on sales targets and customer satisfaction",
                        "benefits": "Health insurance, free coffee, training opportunities",
                    },
                },
                "sales_metrics": {
                    "key_performance_indicators": [
                        "Daily sales revenue",
                        "Customer acquisition cost (CAC)",
                        "Customer lifetime value (CLV)",
                        "Average transaction value",
                        "Customer retention rate",
                        "Sales conversion rate",
                        "Social media engagement",
                        "Online review ratings",
                    ],
                    "targets": {
                        "monthly_revenue": "250,000 THB",
                        "customer_acquisition": "100 new customers/month",
                        "retention_rate": "70%",
                        "average_transaction": "150 THB",
                    },
                },
                "partnerships": {
                    "local_businesses": [
                        {
                            "type": "Co-working spaces",
                            "benefit": "Regular corporate customers",
                            "approach": "Exclusive discounts and delivery",
                        },
                        {
                            "type": "Gyms and fitness centers",
                            "benefit": "Health-conscious customers",
                            "approach": "Post-workout refreshments",
                        },
                        {
                            "type": "Local offices",
                            "benefit": "Bulk orders and regular customers",
                            "approach": "Corporate catering and coffee subscriptions",
                        },
                    ],
                    "suppliers": [
                        {
                            "type": "Coffee bean suppliers",
                            "benefit": "Quality assurance and competitive pricing",
                            "approach": "Long-term contracts and volume discounts",
                        },
                        {
                            "type": "Equipment suppliers",
                            "benefit": "Reliable equipment and maintenance",
                            "approach": "Service contracts and training",
                        },
                    ],
                },
                "recommendations": [
                    "Focus on building strong relationships with local customers",
                    "Implement a comprehensive digital marketing strategy",
                    "Develop a loyalty program to increase customer retention",
                    "Train staff in sales techniques and customer service",
                    "Build partnerships with local businesses for mutual benefit",
                    "Monitor and respond to customer feedback regularly",
                    "Invest in technology for better customer experience",
                    "Create unique experiences that differentiate from competitors",
                ],
                "ai_analysis": sales_analysis_text,
            }

            return sales_strategy

        except Exception as e:
            # Fallback to predefined sales strategy if OpenAI fails
            return {
                "business_name": business_name,
                "target_customer_segments": {
                    "primary": "Young professionals and students",
                    "secondary": "Local residents",
                },
                "sales_channels": {
                    "direct": "In-store sales",
                    "digital": "Online ordering and delivery",
                },
                "customer_acquisition": [
                    "Social media marketing",
                    "Local partnerships",
                    "Word-of-mouth referrals",
                ],
                "recommendations": [
                    "Build strong customer relationships",
                    "Implement loyalty program",
                    "Focus on digital marketing",
                    "Train staff in sales techniques",
                ],
            }


# Initialize sales agent
sales_agent = SalesAgent()


@app.post("/receive_message", response_model=SalesResponse)
async def receive_message(message: MCPMessage):
    """Receive and process messages from Core Agent"""
    try:
        sales_strategy = await sales_agent.analyze_sales_strategy(
            message.business_data, message.strategic_plan
        )

        return SalesResponse(
            agent_type=message.agent_type,
            sales_strategy=sales_strategy,
            timestamp=datetime.now().isoformat(),
            request_id=message.request_id,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Sales analysis failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_type": "sales",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5004)
