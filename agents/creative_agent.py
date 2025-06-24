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

app = FastAPI(title="Creative Agent", version="1.0.0")

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
        business_type = business_data.get("business_type", "")
        location = business_data.get("location", "")
        description = business_data.get("description", "")
        target_market = business_data.get("target_market", "")
        competitors = business_data.get("competitors", [])
        industry = business_data.get("industry", "")
        business_model = business_data.get("business_model", "")
        unique_value_proposition = business_data.get("unique_value_proposition", "")

        # Create dynamic prompt for creative analysis
        prompt = f"""
        As a creative marketing and branding expert, analyze the following business and provide creative recommendations:

        Business Information:
        - Name: {business_name}
        - Type: {business_type}
        - Location: {location}
        - Description: {description}
        - Target Market: {target_market}
        - Industry: {industry}
        - Business Model: {business_model}
        - Unique Value Proposition: {unique_value_proposition}
        - Competitors: {', '.join(competitors)}
        
        Strategic Plan Context: {strategic_plan.get('competitive_positioning', {}).get('unique_value_proposition', '')}

        Please provide creative analysis specifically tailored for this {business_type} business in the {industry} industry, including:

        1. Brand Identity Recommendations:
           - Brand personality and voice
           - Brand values and positioning
           - Visual identity elements

        2. Marketing Campaign Ideas:
           - Campaign concepts and themes
           - Marketing channels and tactics
           - Seasonal and promotional campaigns

        3. Visual Design Suggestions:
           - Visual style and aesthetics
           - Color palette and typography
           - Brand consistency guidelines

        4. Content Marketing Strategy:
           - Content themes and topics
           - Messaging framework
           - Storytelling approach

        5. Social Media Approach:
           - Platform strategy
           - Content calendar
           - Engagement tactics

        6. Customer Engagement Tactics:
           - Loyalty programs
           - Community building
           - Interactive experiences

        7. Creative Differentiation Ideas:
           - Unique creative elements
           - Competitive advantages
           - Innovation opportunities

        Focus on creative ways to stand out from competitors and build a strong brand presence for this {business_type} business in the {industry} industry.
        """

        try:
            # Call OpenAI for creative analysis
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert creative marketing consultant specializing in brand development, visual design, and innovative marketing strategies for {business_type} businesses in the {industry} industry. Provide specific, actionable creative recommendations tailored to this business type and industry.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1500,
                temperature=0.8,
            )

            creative_analysis_text = response.choices[0].message.content

            # Create dynamic creative analysis structure
            creative_analysis = {
                "business_name": business_name,
                "business_type": business_type,
                "brand_identity": {
                    "brand_personality": f"Professional, innovative, and {business_type}-focused",
                    "brand_values": [
                        f"Quality {business_type} services",
                        "Customer satisfaction",
                        "Innovation and excellence",
                        "Industry expertise",
                    ],
                    "brand_voice": "Professional, knowledgeable, and approachable",
                    "color_palette": {
                        "primary": "#2E86AB",  # Professional Blue
                        "secondary": "#A23B72",  # Modern Purple
                        "accent": "#F18F01",  # Energetic Orange
                    },
                    "logo_concept": f"Modern, professional design incorporating {business_type} elements with industry-specific touches",
                },
                "marketing_campaigns": [
                    {
                        "campaign_name": f"{business_type.title()} Excellence",
                        "concept": f"Highlight the quality and expertise in {business_type} services",
                        "channels": [
                            "Social media",
                            "Industry partnerships",
                            "Professional events",
                        ],
                        "duration": "3 months",
                    },
                    {
                        "campaign_name": f"{industry} Innovation",
                        "concept": f"Position the business as an innovative leader in {industry}",
                        "channels": [
                            "Industry events",
                            "Professional networks",
                            "Digital marketing",
                        ],
                        "duration": "Ongoing",
                    },
                    {
                        "campaign_name": f"{business_type} Success Stories",
                        "concept": f"Showcase successful {business_type} projects and client outcomes",
                        "channels": [
                            "Case studies",
                            "Client testimonials",
                            "Professional content",
                        ],
                        "duration": "6 months",
                    },
                ],
                "visual_design": {
                    "brand_identity": f"Professional, modern design reflecting {business_type} expertise",
                    "marketing_materials": f"Consistent branding across all {business_type} materials",
                    "digital_presence": f"Clean, professional website and social media presence",
                    "presentation_materials": f"Professional templates for {business_type} presentations",
                },
                "content_strategy": {
                    "blog_topics": [
                        f"{business_type} industry insights",
                        f"Best practices in {industry}",
                        f"Success stories and case studies",
                        f"{business_type} trends and innovations",
                    ],
                    "social_media_content": [
                        f"{business_type} service highlights",
                        "Client testimonials and reviews",
                        f"Industry expertise and thought leadership",
                        f"{business_type} project showcases",
                    ],
                    "video_content": [
                        f"{business_type} service demonstrations",
                        "Client success stories",
                        f"Industry insights and analysis",
                        f"{business_type} process explanations",
                    ],
                },
                "social_media_strategy": {
                    "platforms": ["LinkedIn", "Facebook", "Instagram", "Twitter"],
                    "content_calendar": "Professional content with industry insights",
                    "engagement_tactics": [
                        "Thought leadership content",
                        "Industry discussions and insights",
                        "Client success stories",
                        "Professional networking",
                    ],
                },
                "customer_engagement": {
                    "loyalty_program": f"{business_type} Excellence Program with rewards and recognition",
                    "events": [
                        f"{business_type} workshops and training",
                        f"Industry networking events",
                        f"Client appreciation events",
                        f"{business_type} innovation showcases",
                    ],
                    "personalization": f"Tailored {business_type} solutions and personalized service recommendations",
                },
                "creative_differentiation": [
                    f"Specialized {business_type} expertise and knowledge",
                    f"Industry-specific {business_type} solutions",
                    f"Innovative {business_type} approaches and methodologies",
                    f"Professional {business_type} service delivery",
                    f"Thought leadership in {industry}",
                ],
                "recommendations": [
                    f"Develop a strong professional brand identity for {business_type} services",
                    f"Create engaging content that showcases {business_type} expertise",
                    f"Build thought leadership in the {industry} industry",
                    f"Establish professional partnerships and networks",
                    f"Implement a customer success program for {business_type} clients",
                    f"Focus on innovation and excellence in {business_type} delivery",
                    f"Create educational content about {business_type} and {industry} trends",
                ],
                "ai_analysis": creative_analysis_text,
            }

            return creative_analysis

        except Exception as e:
            # Fallback to dynamic creative analysis if OpenAI fails
            return {
                "business_name": business_name,
                "business_type": business_type,
                "brand_identity": {
                    "brand_personality": f"Professional and {business_type}-focused",
                    "brand_values": [
                        f"Quality {business_type} services",
                        "Excellence",
                        "Innovation",
                    ],
                    "color_palette": {"primary": "#2E86AB", "secondary": "#A23B72"},
                },
                "marketing_campaigns": [
                    {
                        "campaign_name": f"{business_type} Excellence",
                        "concept": f"Highlight {business_type} quality and expertise",
                    }
                ],
                "recommendations": [
                    f"Develop strong professional brand identity for {business_type}",
                    f"Create engaging content showcasing {business_type} expertise",
                    f"Build thought leadership in {industry}",
                    f"Focus on {business_type} service excellence",
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
