from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import openai
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(title="Creative Agent", version="1.0.0")

# Configure OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")


class MCPMessage(BaseModel):
    agent_type: str
    business_data: Dict[str, Any]
    strategic_plan: Dict[str, Any] = {}
    timestamp: str
    request_id: str


class CreativeResponse(BaseModel):
    agent_type: str
    creative_analysis: Dict[str, Any]
    timestamp: str
    request_id: str


class CreativeAgent:
    """Creative Agent for marketing and branding analysis"""

    def __init__(self):
        self.agent_type = "creative"

    async def analyze_creative_aspects(
        self, business_data: Dict[str, Any], strategic_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze creative aspects of the business"""

        business_name = business_data.get("business_name", "")
        location = business_data.get("location", "")
        competitors = business_data.get("competitors", [])

        # Create prompt for creative analysis
        prompt = f"""
        As a creative marketing and branding expert, analyze the following business and provide creative recommendations:

        Business Name: {business_name}
        Location: {location}
        Competitors: {', '.join(competitors)}
        
        Strategic Plan Context: {strategic_plan.get('competitive_positioning', {}).get('unique_value_proposition', '')}

        Please provide creative analysis including:
        1. Brand identity recommendations
        2. Marketing campaign ideas
        3. Visual design suggestions
        4. Content marketing strategy
        5. Social media approach
        6. Customer engagement tactics
        7. Creative differentiation ideas

        Focus on creative ways to stand out from competitors and build a strong brand presence.
        """

        try:
            # Call OpenAI for creative analysis
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert creative marketing consultant specializing in brand development, visual design, and innovative marketing strategies.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1200,
                temperature=0.8,
            )

            creative_analysis_text = response.choices[0].message.content

            # Structure the creative analysis
            creative_analysis = {
                "business_name": business_name,
                "brand_identity": {
                    "brand_personality": "Friendly, welcoming, and community-focused",
                    "brand_values": [
                        "Quality coffee and service",
                        "Community building",
                        "Sustainability",
                        "Customer satisfaction",
                    ],
                    "brand_voice": "Warm, approachable, and knowledgeable",
                    "color_palette": {
                        "primary": "#8B4513",  # Saddle Brown
                        "secondary": "#DEB887",  # Burlywood
                        "accent": "#D2691E",  # Chocolate
                    },
                    "logo_concept": "Modern, minimalist design incorporating coffee elements with Thai cultural touches",
                },
                "marketing_campaigns": [
                    {
                        "campaign_name": "Morning Ritual",
                        "concept": "Celebrate the daily coffee ritual with local customers",
                        "channels": [
                            "Social media",
                            "Local partnerships",
                            "In-store events",
                        ],
                        "duration": "3 months",
                    },
                    {
                        "campaign_name": "Community Corner",
                        "concept": "Position the cafe as a community gathering space",
                        "channels": [
                            "Local events",
                            "Partnerships with nearby businesses",
                            "Social media",
                        ],
                        "duration": "Ongoing",
                    },
                    {
                        "campaign_name": "Thai Coffee Heritage",
                        "concept": "Highlight Thai coffee culture and traditions",
                        "channels": [
                            "Content marketing",
                            "Cultural events",
                            "Tourism partnerships",
                        ],
                        "duration": "6 months",
                    },
                ],
                "visual_design": {
                    "store_interior": "Warm, rustic design with modern touches",
                    "packaging": "Eco-friendly materials with Thai-inspired patterns",
                    "menu_design": "Clean, readable layout with beautiful food photography",
                    "digital_assets": "Consistent visual style across all platforms",
                },
                "content_strategy": {
                    "blog_topics": [
                        "Coffee brewing techniques",
                        "Local coffee culture",
                        "Behind-the-scenes stories",
                        "Customer spotlights",
                    ],
                    "social_media_content": [
                        "Daily coffee photos",
                        "Customer testimonials",
                        "Staff stories",
                        "Local community events",
                    ],
                    "video_content": [
                        "Coffee preparation videos",
                        "Store atmosphere tours",
                        "Customer interviews",
                        "Behind-the-scenes content",
                    ],
                },
                "social_media_strategy": {
                    "platforms": ["Facebook", "Instagram", "Line", "TikTok"],
                    "content_calendar": "Daily posts with weekly themes",
                    "engagement_tactics": [
                        "User-generated content campaigns",
                        "Interactive polls and questions",
                        "Live streaming events",
                        "Influencer partnerships",
                    ],
                },
                "customer_engagement": {
                    "loyalty_program": "Coffee Passport with rewards and challenges",
                    "events": [
                        "Coffee tasting sessions",
                        "Barista workshops",
                        "Local artist exhibitions",
                        "Community meetups",
                    ],
                    "personalization": "Remember customer preferences and offer personalized recommendations",
                },
                "creative_differentiation": [
                    "Thai-inspired coffee blends",
                    "Local art exhibitions in the cafe",
                    "Community bulletin board",
                    "Seasonal Thai festival celebrations",
                    "Partnership with local musicians for live performances",
                ],
                "recommendations": [
                    "Develop a strong visual brand identity with consistent colors and typography",
                    "Create engaging social media content that tells your story",
                    "Host regular community events to build customer loyalty",
                    "Partner with local artists and musicians for unique experiences",
                    "Implement a customer loyalty program with gamification elements",
                    "Focus on sustainability and eco-friendly practices in branding",
                    "Create educational content about coffee and Thai culture",
                ],
                "ai_analysis": creative_analysis_text,
            }

            return creative_analysis

        except Exception as e:
            # Fallback to predefined creative analysis if OpenAI fails
            return {
                "business_name": business_name,
                "brand_identity": {
                    "brand_personality": "Friendly and welcoming",
                    "brand_values": ["Quality", "Community", "Service"],
                    "color_palette": {"primary": "#8B4513", "secondary": "#DEB887"},
                },
                "marketing_campaigns": [
                    {
                        "campaign_name": "Community Focus",
                        "concept": "Build local community connections",
                    }
                ],
                "recommendations": [
                    "Develop strong visual brand identity",
                    "Create engaging social media content",
                    "Host community events",
                    "Focus on customer experience",
                ],
            }


# Initialize creative agent
creative_agent = CreativeAgent()


@app.post("/receive_message", response_model=CreativeResponse)
async def receive_message(message: MCPMessage):
    """Receive and process messages from Core Agent"""
    try:
        creative_analysis = await creative_agent.analyze_creative_aspects(
            message.business_data, message.strategic_plan
        )

        return CreativeResponse(
            agent_type=message.agent_type,
            creative_analysis=creative_analysis,
            timestamp=datetime.now().isoformat(),
            request_id=message.request_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Creative analysis failed: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_type": "creative",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5002)
