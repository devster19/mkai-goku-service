"""
Agent utilities for business analysis
These are callable functions that don't require separate HTTP servers
"""

import os
import openai
from typing import Dict, Any, List
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI - handle missing API key gracefully
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    try:
        client = openai.OpenAI(api_key=api_key)
        OPENAI_AVAILABLE = True
        print("✅ OpenAI API configured successfully")
    except Exception as e:
        print(f"⚠️ OpenAI configuration failed: {e}")
        OPENAI_AVAILABLE = False
else:
    print("⚠️ OPENAI_API_KEY not found in environment variables")
    OPENAI_AVAILABLE = False


async def analyze_strategic(business_data: Dict[str, Any], context: Dict[str, Any] = None) -> Dict[str, Any]:
    """Strategic agent for business strategy planning"""
    
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
    - Initial Investment: {f"${initial_investment:,.0f}" if initial_investment else "Not specified"}
    - Team Size: {f"{team_size} employees" if team_size else "Not specified"}
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
        if OPENAI_AVAILABLE:
            # Call OpenAI for strategic analysis using new API
            response = client.chat.completions.create(
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
        else:
            strategic_analysis = f"Strategic analysis for {business_name} - {business_type} business in {location}"

        # Create strategic plan structure
        strategic_plan = {
            "business_name": business_name,
            "business_type": business_type,
            "location": location,
            "market_analysis": {
                "target_market": target_market,
                "market_size": market_size or "To be determined",
                "market_trends": f"Industry-specific trends for {industry}",
                "analysis_text": strategic_analysis,
            },
            "competitive_positioning": {
                "unique_value_proposition": unique_value_proposition or f"Quality {business_type} services",
                "competitive_advantages": [
                    f"Specialized {business_type} expertise",
                    f"Strong market positioning in {location}",
                    "Customer-focused approach",
                ],
                "differentiation_strategy": f"Focus on {business_type} excellence and customer experience",
            },
            "growth_strategy": {
                "short_term_goals": growth_goals or [
                    f"Establish {business_type} market presence",
                    "Build customer base",
                    "Develop operational processes",
                ],
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
                "phase_1": ["Market research and validation", "Business setup and licensing", "Initial team hiring"],
                "phase_2": ["Launch operations", "Marketing campaigns", "Customer acquisition"],
                "phase_3": ["Scale operations", "Process optimization", "Market expansion"],
            },
            "key_recommendations": [
                "Focus on market research and customer validation",
                "Develop a clear competitive advantage",
                "Build strong partnerships and alliances",
                "Invest in technology and innovation",
                "Create a strong brand identity",
                "Implement data-driven decision making",
            ],
        }

        return {"strategic_plan": strategic_plan}

    except Exception as e:
        print(f"Error in strategic analysis: {e}")
        # Return fallback response
        return {
            "strategic_plan": {
                "business_name": business_name,
                "vision": f"To become a leading {business_type} in the market",
                "mission": f"To provide exceptional value to our customers",
                "goals": ["Increase market share", "Improve customer satisfaction", "Expand operations"],
                "strategies": ["Market penetration", "Product development", "Strategic partnerships"],
                "key_recommendations": [
                    "Focus on market research and customer validation",
                    "Develop a clear competitive advantage",
                    "Build strong partnerships and alliances",
                    "Invest in technology and innovation"
                ]
            }
        }


async def analyze_swot(business_data: Dict[str, Any], strategic_plan: Dict[str, Any] = None) -> Dict[str, Any]:
    """SWOT agent for business analysis"""
    
    business_name = business_data.get("business_name", "")
    business_type = business_data.get("business_type", "")
    location = business_data.get("location", "")
    target_market = business_data.get("target_market", "")
    competitors = business_data.get("competitors", [])
    unique_value_proposition = business_data.get("unique_value_proposition", "")
    initial_investment = business_data.get("initial_investment")
    team_size = business_data.get("team_size")

    prompt = f"""
    As a business analyst, conduct a comprehensive SWOT analysis for the following business:

    Business: {business_name}
    Type: {business_type}
    Location: {location}
    Target Market: {target_market}
    Competitors: {', '.join(competitors)}
    Unique Value Proposition: {unique_value_proposition}
    Initial Investment: {f"${initial_investment:,.0f}" if initial_investment else "Not specified"}
    Team Size: {f"{team_size} employees" if team_size else "Not specified"}

    Strategic Context: {strategic_plan.get('vision', '') if strategic_plan else 'Not available'}

    Please provide a detailed SWOT analysis with:
    1. Strengths (internal positive factors)
    2. Weaknesses (internal negative factors)
    3. Opportunities (external positive factors)
    4. Threats (external negative factors)
    5. Action plan based on the analysis

    Focus on specific, actionable insights for this {business_type} business.
    """

    try:
        if OPENAI_AVAILABLE:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert business analyst specializing in SWOT analysis for {business_type} businesses. Provide detailed, actionable insights.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1500,
                temperature=0.7,
            )

            swot_analysis_text = response.choices[0].message.content
        else:
            swot_analysis_text = f"SWOT analysis for {business_name} - {business_type} business"

        return {
            "swot_analysis": {
                "strengths": [
                    "Strong business concept",
                    "Clear target market",
                    "Unique value proposition",
                    f"Specialized {business_type} expertise",
                ],
                "weaknesses": [
                    "Limited initial resources",
                    "New market entry",
                    "Need for brand recognition",
                    "Limited operational experience",
                ],
                "opportunities": [
                    "Growing market demand",
                    "Technology advancement",
                    "Market expansion potential",
                    "Online presence opportunities",
                ],
                "threats": [
                    "Competition from established players",
                    "Market volatility",
                    "Regulatory changes",
                    "Economic uncertainty",
                ],
                "action_plan": {
                    "immediate_actions": [
                        "Leverage strengths to capitalize on opportunities",
                        "Address weaknesses through strategic planning",
                        "Develop contingency plans for identified threats",
                        "Focus on building competitive advantages",
                    ],
                    "analysis_text": swot_analysis_text,
                }
            }
        }

    except Exception as e:
        print(f"Error in SWOT analysis: {e}")
        return {
            "swot_analysis": {
                "strengths": ["Strong business concept", "Clear target market", "Unique value proposition"],
                "weaknesses": ["Limited initial resources", "New market entry", "Need for brand recognition"],
                "opportunities": ["Growing market demand", "Technology advancement", "Market expansion"],
                "threats": ["Competition", "Market volatility", "Regulatory changes"],
                "action_plan": {
                    "immediate_actions": [
                        "Leverage strengths to capitalize on opportunities",
                        "Address weaknesses through strategic planning",
                        "Develop contingency plans for identified threats",
                        "Focus on building competitive advantages",
                    ]
                }
            }
        }


async def analyze_business_model(business_data: Dict[str, Any], strategic_plan: Dict[str, Any] = None, swot_analysis: Dict[str, Any] = None) -> Dict[str, Any]:
    """Business Model Canvas agent"""
    
    business_name = business_data.get("business_name", "")
    business_type = business_data.get("business_type", "")
    target_market = business_data.get("target_market", "")
    business_model = business_data.get("business_model", "")
    unique_value_proposition = business_data.get("unique_value_proposition", "")

    prompt = f"""
    Create a comprehensive Business Model Canvas for:

    Business: {business_name}
    Type: {business_type}
    Target Market: {target_market}
    Business Model: {business_model}
    Value Proposition: {unique_value_proposition}

    Strategic Context: {strategic_plan.get('vision', '') if strategic_plan else 'Not available'}
    SWOT Analysis: {swot_analysis.get('strengths', []) if swot_analysis else 'Not available'}

    Please provide a detailed Business Model Canvas with all 9 building blocks:
    1. Key Partners
    2. Key Activities
    3. Value Propositions
    4. Customer Relationships
    5. Customer Segments
    6. Key Resources
    7. Channels
    8. Cost Structure
    9. Revenue Streams

    Also include key insights and recommendations based on the business model.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are an expert in Business Model Canvas creation for {business_type} businesses. Provide comprehensive, actionable business model insights.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=1500,
            temperature=0.7,
        )

        bmc_analysis_text = response.choices[0].message.content

        return {
            "business_model_canvas": {
                "key_partners": ["Suppliers", "Technology providers", "Marketing partners", "Service providers"],
                "key_activities": ["Product development", "Marketing", "Customer service", "Operations management"],
                "value_propositions": ["Quality products", "Excellent service", "Competitive pricing", unique_value_proposition or f"Superior {business_type} experience"],
                "customer_relationships": ["Personal assistance", "Self-service", "Community", "Co-creation"],
                "customer_segments": [target_market or "General market"],
                "key_resources": ["Human resources", "Technology", "Brand", "Intellectual property"],
                "channels": ["Online", "Direct sales", "Partnerships", "Social media"],
                "cost_structure": ["Operational costs", "Marketing", "Technology", "Human resources"],
                "revenue_streams": ["Product sales", "Service fees", "Subscriptions", "Consulting"],
                "key_insights": {
                    "recommendations": [
                        "Optimize revenue streams and pricing strategy",
                        "Strengthen key partnerships and relationships",
                        "Focus on customer acquisition and retention",
                        "Streamline operations to reduce costs",
                    ],
                    "analysis_text": bmc_analysis_text,
                }
            }
        }

    except Exception as e:
        print(f"Error in Business Model Canvas analysis: {e}")
        return {
            "business_model_canvas": {
                "key_partners": ["Suppliers", "Technology providers", "Marketing partners"],
                "key_activities": ["Product development", "Marketing", "Customer service"],
                "value_propositions": ["Quality products", "Excellent service", "Competitive pricing"],
                "customer_relationships": ["Personal assistance", "Self-service", "Community"],
                "customer_segments": [target_market or "General market"],
                "key_resources": ["Human resources", "Technology", "Brand"],
                "channels": ["Online", "Direct sales", "Partnerships"],
                "cost_structure": ["Operational costs", "Marketing", "Technology"],
                "revenue_streams": ["Product sales", "Service fees", "Subscriptions"],
                "key_insights": {
                    "recommendations": [
                        "Optimize revenue streams and pricing strategy",
                        "Strengthen key partnerships and relationships",
                        "Focus on customer acquisition and retention",
                        "Streamline operations to reduce costs",
                    ]
                }
            }
        }


async def analyze_creative(business_data: Dict[str, Any], strategic_plan: Dict[str, Any] = None) -> Dict[str, Any]:
    """Creative agent for branding and marketing"""
    
    business_name = business_data.get("business_name", "")
    business_type = business_data.get("business_type", "")
    target_market = business_data.get("target_market", "")
    unique_value_proposition = business_data.get("unique_value_proposition", "")

    prompt = f"""
    As a creative marketing expert, provide creative analysis and recommendations for:

    Business: {business_name}
    Type: {business_type}
    Target Market: {target_market}
    Value Proposition: {unique_value_proposition}

    Strategic Context: {strategic_plan.get('vision', '') if strategic_plan else 'Not available'}

    Please provide:
    1. Brand identity recommendations
    2. Creative marketing ideas
    3. Unique angles and positioning
    4. Content strategy suggestions
    5. Visual identity concepts
    6. Marketing campaign ideas

    Focus on creative, innovative approaches that will help this {business_type} stand out in the market.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a creative marketing expert specializing in {business_type} businesses. Provide innovative, creative solutions that will help businesses stand out.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=1500,
            temperature=0.8,
        )

        creative_analysis_text = response.choices[0].message.content

        return {
            "creative_analysis": {
                "brand_identity": f"Modern, innovative {business_type}",
                "marketing_ideas": [
                    "Social media campaigns",
                    "Influencer partnerships",
                    "Content marketing",
                    "Video marketing",
                    "Interactive experiences",
                ],
                "unique_angles": [
                    "Customer-centric approach",
                    "Technology integration",
                    "Sustainability focus",
                    "Community building",
                ],
                "content_strategy": [
                    "Educational content",
                    "Behind-the-scenes content",
                    "Customer testimonials",
                    "Industry insights",
                ],
                "visual_concepts": [
                    "Modern, clean design",
                    "Bold color palette",
                    "Professional photography",
                    "Consistent branding",
                ],
                "campaign_ideas": [
                    "Launch campaign",
                    "Seasonal promotions",
                    "Referral programs",
                    "Loyalty programs",
                ],
                "recommendations": [
                    "Develop a strong, memorable brand identity",
                    "Create engaging content marketing strategies",
                    "Leverage social media and digital platforms",
                    "Focus on customer experience and satisfaction",
                    "Build community and engagement",
                ],
                "analysis_text": creative_analysis_text,
            }
        }

    except Exception as e:
        print(f"Error in creative analysis: {e}")
        return {
            "creative_analysis": {
                "brand_identity": f"Modern, innovative {business_type}",
                "marketing_ideas": ["Social media campaigns", "Influencer partnerships", "Content marketing"],
                "unique_angles": ["Customer-centric approach", "Technology integration", "Sustainability focus"],
                "recommendations": [
                    "Develop a strong, memorable brand identity",
                    "Create engaging content marketing strategies",
                    "Leverage social media and digital platforms",
                    "Focus on customer experience and satisfaction"
                ]
            }
        }


async def analyze_financial(business_data: Dict[str, Any], strategic_plan: Dict[str, Any] = None) -> Dict[str, Any]:
    """Financial agent for financial analysis"""
    
    business_name = business_data.get("business_name", "")
    business_type = business_data.get("business_type", "")
    initial_investment = business_data.get("initial_investment")
    team_size = business_data.get("team_size")

    prompt = f"""
    As a financial analyst, provide comprehensive financial analysis for:

    Business: {business_name}
    Type: {business_type}
    Initial Investment: {f"${initial_investment:,.0f}" if initial_investment else "Not specified"}
    Team Size: {f"{team_size} employees" if team_size else "Not specified"}

    Strategic Context: {strategic_plan.get('vision', '') if strategic_plan else 'Not available'}

    Please provide:
    1. Financial projections and forecasts
    2. Break-even analysis
    3. Funding recommendations
    4. Cost structure analysis
    5. Revenue model optimization
    6. Financial risk assessment
    7. Key financial metrics and KPIs

    Focus on practical, actionable financial advice for this {business_type} business.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a financial analyst specializing in {business_type} businesses. Provide practical, actionable financial advice and projections.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=1500,
            temperature=0.7,
        )

        financial_analysis_text = response.choices[0].message.content

        return {
            "financial_analysis": {
                "startup_costs": initial_investment or 50000,
                "projected_revenue": "To be determined based on market analysis",
                "break_even_analysis": "6-12 months projected",
                "funding_recommendations": [
                    "Bootstrap initially",
                    "Seek angel investment",
                    "Consider crowdfunding",
                    "Explore small business loans",
                ],
                "cost_structure": {
                    "fixed_costs": ["Rent", "Utilities", "Insurance", "Software subscriptions"],
                    "variable_costs": ["Materials", "Labor", "Marketing", "Commissions"],
                },
                "revenue_model": {
                    "primary_streams": ["Product sales", "Service fees"],
                    "secondary_streams": ["Consulting", "Training", "Licensing"],
                },
                "financial_projections": {
                    "year_1": {
                        "revenue": initial_investment * 2 if initial_investment else 100000,
                        "expenses": initial_investment * 1.5 if initial_investment else 75000,
                        "profit_margin": "25%",
                    },
                    "year_2": {
                        "revenue": initial_investment * 4 if initial_investment else 200000,
                        "expenses": initial_investment * 3 if initial_investment else 150000,
                        "profit_margin": "30%",
                    },
                    "year_3": {
                        "revenue": initial_investment * 6 if initial_investment else 300000,
                        "expenses": initial_investment * 4.5 if initial_investment else 225000,
                        "profit_margin": "35%",
                    },
                },
                "recommendations": [
                    "Maintain strict financial discipline and budgeting",
                    "Diversify funding sources and revenue streams",
                    "Monitor cash flow and financial metrics closely",
                    "Plan for scalability and growth investments",
                    "Build emergency fund for unexpected expenses",
                ],
                "analysis_text": financial_analysis_text,
            }
        }

    except Exception as e:
        print(f"Error in financial analysis: {e}")
        return {
            "financial_analysis": {
                "startup_costs": initial_investment or 50000,
                "projected_revenue": "To be determined based on market analysis",
                "break_even_analysis": "6-12 months projected",
                "funding_recommendations": ["Bootstrap initially", "Seek angel investment", "Consider crowdfunding"],
                "recommendations": [
                    "Maintain strict financial discipline and budgeting",
                    "Diversify funding sources and revenue streams",
                    "Monitor cash flow and financial metrics closely",
                    "Plan for scalability and growth investments"
                ]
            }
        }


async def analyze_sales(business_data: Dict[str, Any], strategic_plan: Dict[str, Any] = None) -> Dict[str, Any]:
    """Sales agent for sales strategy"""
    
    business_name = business_data.get("business_name", "")
    business_type = business_data.get("business_type", "")
    target_market = business_data.get("target_market", "")
    business_model = business_data.get("business_model", "")

    prompt = f"""
    As a sales strategy expert, provide comprehensive sales strategy for:

    Business: {business_name}
    Type: {business_type}
    Target Market: {target_market}
    Business Model: {business_model}

    Strategic Context: {strategic_plan.get('vision', '') if strategic_plan else 'Not available'}

    Please provide:
    1. Sales strategy and approach
    2. Target customer segments
    3. Sales channels and methods
    4. Pricing strategy
    5. Sales process and pipeline
    6. Lead generation strategies
    7. Customer acquisition tactics
    8. Sales team structure and training

    Focus on practical, effective sales strategies for this {business_type} business.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a sales strategy expert specializing in {business_type} businesses. Provide practical, effective sales strategies and tactics.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=1500,
            temperature=0.7,
        )

        sales_analysis_text = response.choices[0].message.content

        return {
            "sales_strategy": {
                "target_customers": [target_market or "General market"],
                "sales_channels": [
                    "Direct sales",
                    "Online platform",
                    "Partnerships",
                    "Social media",
                    "Referrals",
                ],
                "pricing_strategy": "Competitive pricing with value-based options",
                "sales_process": [
                    "Lead generation",
                    "Qualification",
                    "Presentation",
                    "Closing",
                    "Follow-up",
                ],
                "lead_generation": [
                    "Content marketing",
                    "Social media advertising",
                    "Networking events",
                    "Referral programs",
                    "Cold outreach",
                ],
                "customer_acquisition": [
                    "Free trials",
                    "Discounts for early adopters",
                    "Referral incentives",
                    "Partnership marketing",
                    "Content marketing",
                ],
                "sales_team": {
                    "structure": "Small, focused team",
                    "training": ["Product knowledge", "Sales techniques", "Customer service"],
                    "incentives": ["Commission-based", "Performance bonuses", "Career growth"],
                },
                "recommendations": [
                    "Develop a comprehensive sales strategy and process",
                    "Build strong relationships with target customers",
                    "Implement effective lead generation and qualification",
                    "Focus on value-based selling and customer success",
                    "Invest in sales team training and development",
                ],
                "analysis_text": sales_analysis_text,
            }
        }

    except Exception as e:
        print(f"Error in sales analysis: {e}")
        return {
            "sales_strategy": {
                "target_customers": [target_market or "General market"],
                "sales_channels": ["Direct sales", "Online platform", "Partnerships"],
                "pricing_strategy": "Competitive pricing with value-based options",
                "sales_process": ["Lead generation", "Qualification", "Presentation", "Closing"],
                "recommendations": [
                    "Develop a comprehensive sales strategy and process",
                    "Build strong relationships with target customers",
                    "Implement effective lead generation and qualification",
                    "Focus on value-based selling and customer success"
                ]
            }
        }


async def analyze_analytics(business_data: Dict[str, Any], all_agent_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Analytics agent for comprehensive analysis"""
    
    business_name = business_data.get("business_name", "")
    business_type = business_data.get("business_type", "")
    market_size = business_data.get("market_size", "")
    competitors = business_data.get("competitors", [])

    # Combine insights from all other agents
    strategic_insights = all_agent_data.get("strategic_plan", {}) if all_agent_data else {}
    creative_insights = all_agent_data.get("creative_analysis", {}) if all_agent_data else {}
    financial_insights = all_agent_data.get("financial_analysis", {}) if all_agent_data else {}
    sales_insights = all_agent_data.get("sales_strategy", {}) if all_agent_data else {}
    swot_insights = all_agent_data.get("swot_analysis", {}) if all_agent_data else {}
    bmc_insights = all_agent_data.get("business_model_canvas", {}) if all_agent_data else {}

    prompt = f"""
    As a business analytics expert, provide comprehensive analytics and insights for:

    Business: {business_name}
    Type: {business_type}
    Market Size: {market_size}
    Competitors: {', '.join(competitors)}

    Strategic Analysis: {strategic_insights.get('vision', 'Not available')}
    Creative Analysis: {creative_insights.get('brand_identity', 'Not available')}
    Financial Analysis: {financial_insights.get('startup_costs', 'Not available')}
    Sales Strategy: {sales_insights.get('target_customers', 'Not available')}
    SWOT Analysis: {swot_insights.get('strengths', 'Not available')}
    Business Model: {bmc_insights.get('key_partners', 'Not available')}

    Please provide:
    1. Comprehensive market analysis
    2. Competitive landscape assessment
    3. Success probability analysis
    4. Key performance indicators
    5. Data-driven insights and recommendations
    6. Risk assessment and mitigation
    7. Growth opportunities identification

    Synthesize all the information from different analyses to provide actionable insights.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a business analytics expert specializing in {business_type} businesses. Synthesize multiple analyses to provide comprehensive, data-driven insights.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=1500,
            temperature=0.7,
        )

        analytics_analysis_text = response.choices[0].message.content

        return {
            "analytics_summary": {
                "market_size": market_size or "To be analyzed",
                "competition_level": "Moderate to high",
                "success_probability": {
                    "overall_success_rate": "75%",
                    "market_conditions": "Favorable",
                    "competitive_advantage": "Strong",
                    "execution_risk": "Medium",
                },
                "key_metrics": [
                    "Customer acquisition cost",
                    "Lifetime value",
                    "Conversion rate",
                    "Customer satisfaction score",
                    "Revenue growth rate",
                ],
                "competitive_analysis": f"Analysis of {len(competitors)} competitors in the {business_type} market",
                "key_insights": [
                    "Strong market opportunity",
                    "Clear competitive positioning",
                    "Solid financial foundation",
                    "Effective sales strategy",
                ],
                "recommendations": [
                    "Track and analyze key performance metrics",
                    "Use data-driven insights for decision making",
                    "Monitor market trends and competitive landscape",
                    "Continuously optimize based on performance data",
                    "Implement A/B testing for optimization",
                ],
                "analysis_text": analytics_analysis_text,
            }
        }

    except Exception as e:
        print(f"Error in analytics analysis: {e}")
        return {
            "analytics_summary": {
                "market_size": market_size or "To be analyzed",
                "competition_level": "Moderate to high",
                "success_probability": {"overall_success_rate": "70%"},
                "key_metrics": ["Customer acquisition cost", "Lifetime value", "Conversion rate"],
                "recommendations": [
                    "Track and analyze key performance metrics",
                    "Use data-driven insights for decision making",
                    "Monitor market trends and competitive landscape",
                    "Continuously optimize based on performance data"
                ]
            }
        }


async def analyze_manager(business_data: Dict[str, Any], all_agent_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Manager agent for operational management and dynamic task assignment"""
    
    business_name = business_data.get("business_name", "")
    business_type = business_data.get("business_type", "")
    team_size = business_data.get("team_size")
    target_market = business_data.get("target_market", "")
    unique_value_proposition = business_data.get("unique_value_proposition", "")
    growth_goals = business_data.get("growth_goals", [])

    # Extract insights from all other agents
    strategic_plan = all_agent_data.get("strategic_plan", {}) if all_agent_data else {}
    creative_analysis = all_agent_data.get("creative_analysis", {}) if all_agent_data else {}
    financial_analysis = all_agent_data.get("financial_analysis", {}) if all_agent_data else {}
    sales_strategy = all_agent_data.get("sales_strategy", {}) if all_agent_data else {}
    swot_analysis = all_agent_data.get("swot_analysis", {}) if all_agent_data else {}
    bmc_analysis = all_agent_data.get("business_model_canvas", {}) if all_agent_data else {}
    analytics_summary = all_agent_data.get("analytics_summary", {}) if all_agent_data else {}

    prompt = f"""
    As a senior business manager and project coordinator, analyze the following business and create dynamic task assignments:

    Business: {business_name}
    Type: {business_type}
    Team Size: {f"{team_size} employees" if team_size else "Not specified"}
    Target Market: {target_market}
    Value Proposition: {unique_value_proposition}
    Growth Goals: {', '.join(growth_goals)}

    Strategic Analysis: {strategic_plan.get('vision', 'Not available')}
    Creative Analysis: {creative_analysis.get('brand_identity', 'Not available')}
    Financial Analysis: {financial_analysis.get('startup_costs', 'Not available')}
    Sales Strategy: {sales_strategy.get('target_customers', 'Not available')}
    SWOT Analysis: {swot_analysis.get('strengths', 'Not available')}
    Business Model: {bmc_analysis.get('key_partners', 'Not available')}
    Analytics Summary: {analytics_summary.get('market_size', 'Not available')}

    Based on this comprehensive analysis, create specific, actionable tasks for each agent:

    1. Strategic Agent Tasks:
       - Market research and competitive analysis
       - Strategic planning and goal setting
       - Business model optimization

    2. Creative Agent Tasks:
       - Brand identity development
       - Marketing content creation
       - Visual design and creative assets

    3. Financial Agent Tasks:
       - Financial planning and budgeting
       - Cost analysis and optimization
       - Funding strategy development

    4. Sales Agent Tasks:
       - Sales strategy development
       - Customer acquisition campaigns
       - Sales process optimization

    5. Analytics Agent Tasks:
       - Performance tracking setup
       - Data analysis and insights
       - KPI monitoring systems

    6. SWOT Agent Tasks:
       - Competitive landscape analysis
       - Risk assessment and mitigation
       - Opportunity identification

    7. Business Model Agent Tasks:
       - Revenue model optimization
       - Partnership development
       - Value proposition enhancement

    For each task, provide:
    - Specific, actionable description
    - Priority level (High/Medium/Low)
    - Estimated timeline
    - Expected outcomes
    - Required resources

    Focus on creating tasks that are immediately actionable and will drive business growth.
    """

    try:
        if OPENAI_AVAILABLE:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a senior business manager specializing in {business_type} businesses. Create specific, actionable task assignments that will drive business success.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2000,
                temperature=0.7,
            )

            management_analysis_text = response.choices[0].message.content
        else:
            management_analysis_text = f"Management analysis for {business_name} - {business_type} business"

        # Create dynamic task assignments based on business type and analysis
        dynamic_tasks = _generate_dynamic_tasks(business_data, all_agent_data)

        return {
            "management_summary": {
                "team_structure": f"Team size: {team_size or 'To be determined'}",
                "operational_plan": [
                    "Phase 1: Setup and Launch",
                    "Phase 2: Growth and Optimization", 
                    "Phase 3: Scale and Expansion",
                ],
                "risk_management": [
                    "Market research and validation",
                    "Financial planning and monitoring",
                    "Legal compliance and insurance",
                    "Operational contingency planning",
                ],
                "quality_control": [
                    "Standard operating procedures",
                    "Quality assurance processes",
                    "Customer feedback systems",
                    "Continuous improvement programs",
                ],
                "performance_management": [
                    "KPI tracking and reporting",
                    "Regular performance reviews",
                    "Goal setting and alignment",
                    "Recognition and reward systems",
                ],
                "success_factors": [
                    "Strong leadership and vision",
                    "Clear communication and processes",
                    "Customer focus and satisfaction",
                    "Continuous learning and adaptation",
                ],
                "analysis_text": management_analysis_text,
            },
            "dynamic_task_assignments": dynamic_tasks,
        }

    except Exception as e:
        print(f"Error in management analysis: {e}")
        # Return fallback with basic task assignments
        return {
            "management_summary": {
                "team_structure": f"Team size: {team_size or 'To be determined'}",
                "operational_plan": ["Phase 1: Setup", "Phase 2: Launch", "Phase 3: Scale"],
                "risk_management": ["Market research", "Financial planning", "Legal compliance"],
                "success_factors": ["Strong leadership", "Clear vision", "Customer focus"]
            },
            "dynamic_task_assignments": _generate_dynamic_tasks(business_data, all_agent_data),
        }


def _generate_dynamic_tasks(business_data: Dict[str, Any], all_agent_data: Dict[str, Any] = None) -> Dict[str, Any]:
    """Generate dynamic task assignments based on business type and analysis"""
    
    business_name = business_data.get("business_name", "")
    business_type = business_data.get("business_type", "")
    target_market = business_data.get("target_market", "")
    unique_value_proposition = business_data.get("unique_value_proposition", "")
    growth_goals = business_data.get("growth_goals", [])
    competitors = business_data.get("competitors", [])

    # Base tasks for all business types
    base_tasks = {
        "strategic_agent": [
            {
                "task": f"Conduct comprehensive market research for {business_name}",
                "agent": "strategic_agent",
                "priority": "High",
                "timeline": "2-3 weeks",
                "description": "Analyze market size, competition, and opportunities",
                "expected_outcome": "Market analysis report with strategic recommendations"
            },
            {
                "task": f"Develop strategic growth plan for {business_name}",
                "agent": "strategic_agent", 
                "priority": "High",
                "timeline": "1-2 weeks",
                "description": "Create 12-month strategic roadmap",
                "expected_outcome": "Strategic plan with milestones and KPIs"
            }
        ],
        "creative_agent": [
            {
                "task": f"Create brand identity and visual assets for {business_name}",
                "agent": "creative_agent",
                "priority": "High", 
                "timeline": "2-3 weeks",
                "description": "Design logo, color scheme, and brand guidelines",
                "expected_outcome": "Complete brand identity package"
            },
            {
                "task": f"Develop marketing content strategy for {business_name}",
                "agent": "creative_agent",
                "priority": "Medium",
                "timeline": "1-2 weeks", 
                "description": "Create content calendar and marketing materials",
                "expected_outcome": "Content strategy and initial marketing assets"
            }
        ],
        "financial_agent": [
            {
                "task": f"Create detailed financial projections for {business_name}",
                "agent": "financial_agent",
                "priority": "High",
                "timeline": "1-2 weeks",
                "description": "Develop 3-year financial forecast and budget",
                "expected_outcome": "Financial model with projections and budget"
            },
            {
                "task": f"Analyze cost structure and optimize expenses for {business_name}",
                "agent": "financial_agent", 
                "priority": "Medium",
                "timeline": "1 week",
                "description": "Review and optimize operational costs",
                "expected_outcome": "Cost optimization recommendations"
            }
        ],
        "sales_agent": [
            {
                "task": f"Develop sales strategy and process for {business_name}",
                "agent": "sales_agent",
                "priority": "High",
                "timeline": "2-3 weeks",
                "description": "Create sales funnel and customer acquisition strategy",
                "expected_outcome": "Sales strategy document and process flow"
            },
            {
                "task": f"Launch customer acquisition campaign for {business_name}",
                "agent": "sales_agent",
                "priority": "Medium",
                "timeline": "2-4 weeks",
                "description": "Execute marketing campaigns to acquire customers",
                "expected_outcome": "Customer acquisition pipeline and results"
            }
        ],
        "analytics_agent": [
            {
                "task": f"Set up performance tracking system for {business_name}",
                "agent": "analytics_agent",
                "priority": "High",
                "timeline": "1-2 weeks",
                "description": "Implement KPI tracking and analytics dashboard",
                "expected_outcome": "Analytics dashboard with key metrics"
            },
            {
                "task": f"Analyze customer data and market trends for {business_name}",
                "agent": "analytics_agent",
                "priority": "Medium",
                "timeline": "1 week",
                "description": "Analyze customer behavior and market insights",
                "expected_outcome": "Customer insights and market analysis report"
            }
        ],
        "swot_agent": [
            {
                "task": f"Conduct competitive analysis for {business_name}",
                "agent": "swot_agent",
                "priority": "High",
                "timeline": "1-2 weeks",
                "description": f"Analyze competitors: {', '.join(competitors)}",
                "expected_outcome": "Competitive analysis report with positioning strategy"
            },
            {
                "task": f"Assess risks and opportunities for {business_name}",
                "agent": "swot_agent",
                "priority": "Medium",
                "timeline": "1 week",
                "description": "Identify potential risks and growth opportunities",
                "expected_outcome": "Risk assessment and opportunity analysis"
            }
        ],
        "business_model_agent": [
            {
                "task": f"Optimize revenue model for {business_name}",
                "agent": "business_model_agent",
                "priority": "High",
                "timeline": "1-2 weeks",
                "description": "Review and optimize pricing and revenue streams",
                "expected_outcome": "Optimized revenue model and pricing strategy"
            },
            {
                "task": f"Develop partnership strategy for {business_name}",
                "agent": "business_model_agent",
                "priority": "Medium",
                "timeline": "2-3 weeks",
                "description": "Identify and develop strategic partnerships",
                "expected_outcome": "Partnership strategy and potential partner list"
            }
        ]
    }

    # Add business-type specific tasks
    if business_type == "coffee_shop":
        base_tasks["creative_agent"].append({
            "task": f"Design coffee shop interior concept for {business_name}",
            "agent": "creative_agent",
            "priority": "High",
            "timeline": "2-3 weeks",
            "description": "Create interior design concept and branding materials",
            "expected_outcome": "Interior design concept and visual mockups"
        })
        base_tasks["sales_agent"].append({
            "task": f"Launch coffee shop grand opening campaign for {business_name}",
            "agent": "sales_agent",
            "priority": "High",
            "timeline": "3-4 weeks",
            "description": "Plan and execute grand opening marketing campaign",
            "expected_outcome": "Grand opening campaign with customer acquisition"
        })

    elif business_type == "tech_startup":
        base_tasks["strategic_agent"].append({
            "task": f"Develop fundraising strategy for {business_name}",
            "agent": "strategic_agent",
            "priority": "High",
            "timeline": "2-3 weeks",
            "description": "Create pitch deck and fundraising strategy",
            "expected_outcome": "Pitch deck and investor outreach plan"
        })
        base_tasks["creative_agent"].append({
            "task": f"Create tech product marketing materials for {business_name}",
            "agent": "creative_agent",
            "priority": "High",
            "timeline": "2-3 weeks",
            "description": "Design product website and marketing materials",
            "expected_outcome": "Product website and marketing assets"
        })

    elif business_type == "restaurant":
        base_tasks["creative_agent"].append({
            "task": f"Design restaurant menu and branding for {business_name}",
            "agent": "creative_agent",
            "priority": "High",
            "timeline": "2-3 weeks",
            "description": "Create menu design and restaurant branding",
            "expected_outcome": "Menu design and restaurant branding package"
        })
        base_tasks["sales_agent"].append({
            "task": f"Launch restaurant opening campaign for {business_name}",
            "agent": "sales_agent",
            "priority": "High",
            "timeline": "3-4 weeks",
            "description": "Plan and execute restaurant opening marketing",
            "expected_outcome": "Restaurant opening campaign and customer acquisition"
        })

    elif business_type == "consulting_firm":
        base_tasks["strategic_agent"].append({
            "task": f"Develop thought leadership strategy for {business_name}",
            "agent": "strategic_agent",
            "priority": "High",
            "timeline": "2-3 weeks",
            "description": "Create thought leadership and content strategy",
            "expected_outcome": "Thought leadership plan and content calendar"
        })
        base_tasks["creative_agent"].append({
            "task": f"Create professional consulting website for {business_name}",
            "agent": "creative_agent",
            "priority": "High",
            "timeline": "3-4 weeks",
            "description": "Design professional website and marketing materials",
            "expected_outcome": "Professional website and marketing assets"
        })

    return base_tasks


async def assign_tasks_to_agents(business_data: Dict[str, Any], analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """AI-powered task assignment to agents based on business analysis"""
    
    business_name = business_data.get("business_name", "")
    business_type = business_data.get("business_type", "")
    
    # Extract key insights from analysis
    strategic_plan = analysis_results.get("strategic_plan", {})
    swot_analysis = analysis_results.get("swot_analysis", {})
    financial_analysis = analysis_results.get("financial_analysis", {})
    sales_strategy = analysis_results.get("sales_strategy", {})
    
    prompt = f"""
    As an AI task orchestrator, assign specific tasks to different agents for:

    Business: {business_name}
    Type: {business_type}
    
    Strategic Plan: {strategic_plan.get('vision', 'Not available')}
    SWOT Analysis: {swot_analysis.get('strengths', 'Not available')}
    Financial Analysis: {financial_analysis.get('startup_costs', 'Not available')}
    Sales Strategy: {sales_strategy.get('target_customers', 'Not available')}
    
    Available Agents:
    1. Strategic Agent - Market analysis, goal setting, strategic planning
    2. Financial Agent - Budget planning, financial projections, cost analysis
    3. Sales Agent - Sales strategy, customer acquisition, pipeline management
    4. Creative Agent - Branding, marketing, content creation
    5. Analytics Agent - Data analysis, performance tracking, insights
    6. Manager Agent - Operations, team management, process optimization
    7. SWOT Agent - Competitive analysis, risk assessment
    8. Business Model Agent - Revenue model, partnerships, value proposition
    
    Please assign specific, actionable tasks to each agent based on the business analysis.
    Consider the business type, current situation, and strategic goals.
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI task orchestrator that intelligently assigns business tasks to specialized agents based on business analysis and requirements.",
                },
                {"role": "user", "content": prompt},
            ],
            max_tokens=1500,
            temperature=0.7,
        )

        task_assignment_text = response.choices[0].message.content

        # Create structured task assignments
        task_assignments = {
            "strategic_agent": [
                "Conduct market research and validation",
                "Develop strategic goals and KPIs",
                "Create competitive positioning strategy",
                "Plan market expansion opportunities",
            ],
            "financial_agent": [
                "Create detailed financial projections",
                "Develop budget and cash flow management",
                "Analyze funding requirements and options",
                "Set up financial monitoring systems",
            ],
            "sales_agent": [
                "Develop sales strategy and process",
                "Create lead generation campaigns",
                "Design customer acquisition programs",
                "Build sales team training programs",
            ],
            "creative_agent": [
                "Develop brand identity and guidelines",
                "Create marketing content and campaigns",
                "Design customer engagement strategies",
                "Plan social media and digital presence",
            ],
            "analytics_agent": [
                "Set up performance tracking systems",
                "Create data analysis dashboards",
                "Develop customer insights programs",
                "Monitor competitive landscape",
            ],
            "manager_agent": [
                "Develop operational processes",
                "Create team management systems",
                "Implement quality control measures",
                "Plan risk management strategies",
            ],
            "swot_agent": [
                "Monitor competitive landscape",
                "Track market trends and changes",
                "Assess new opportunities and threats",
                "Update SWOT analysis regularly",
            ],
            "business_model_agent": [
                "Optimize revenue streams",
                "Develop partnership strategies",
                "Enhance value proposition",
                "Scale business model",
            ],
            "assignment_analysis": task_assignment_text,
        }

        return task_assignments

    except Exception as e:
        print(f"Error in task assignment: {e}")
        # Return default task assignments
        return {
            "strategic_agent": ["Market research", "Strategic planning"],
            "financial_agent": ["Financial planning", "Budget management"],
            "sales_agent": ["Sales strategy", "Customer acquisition"],
            "creative_agent": ["Branding", "Marketing"],
            "analytics_agent": ["Performance tracking", "Data analysis"],
            "manager_agent": ["Operations", "Team management"],
            "swot_agent": ["Competitive analysis", "Risk assessment"],
            "business_model_agent": ["Revenue optimization", "Partnerships"],
        } 