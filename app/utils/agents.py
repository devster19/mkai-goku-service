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

    BUSINESS INFORMATION:
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

    RESPONSE FORMAT - Please structure your response exactly as follows:

    MARKET ANALYSIS:
    [Provide 4-6 key market insights including target market assessment, market size, and growth potential]

    COMPETITIVE POSITIONING:
    [Analyze 4-6 competitive advantages and differentiation strategies for this business]

    GROWTH STRATEGY:
    [Outline 3-4 short-term (0-12 months), medium-term (1-3 years), and long-term (3-5 years) goals]

    RISK ASSESSMENT:
    [Identify 4-6 key market and operational risks with mitigation strategies]

    KEY PERFORMANCE INDICATORS:
    [Define 5-7 important KPIs for revenue, customer, and operational metrics]

    IMPLEMENTATION TIMELINE:
    [Provide 3-4 key activities for each phase: Phase 1 (0-6 months), Phase 2 (6-12 months), Phase 3 (12-24 months)]

    RESOURCE REQUIREMENTS:
    [List 4-6 financial, human resource, and technology requirements]

    STRATEGIC RECOMMENDATIONS:
    [Provide 6-8 actionable strategic recommendations with timing and priority:
    - Recommendation: [specific strategic action]
    - Timing: [this week/next week/this month/next month]
    - Priority: [High/Medium/Low - how urgent/rush it is]
    - Expected Impact: [brief description of expected outcome]]

    Focus on providing specific, actionable recommendations that are highly relevant to this {business_type} business in the {industry} industry.
    """

    try:
        if OPENAI_AVAILABLE:
            # Call OpenAI for strategic analysis using new API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert strategic business consultant with deep knowledge of {industry} industry, market analysis, competitive positioning, and business growth strategies. You provide specific, actionable advice tailored to {business_type} businesses. Always respond in the exact format requested with clear sections and strategic insights.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2500,
                temperature=0.7,
            )

            strategic_analysis = response.choices[0].message.content
        else:
            strategic_analysis = f"Strategic analysis for {business_name} - {business_type} business in {location}"

        # Parse the AI response to extract structured data
        sections = strategic_analysis.split('\n\n')
        parsed_data = {}
        
        for section in sections:
            if ':' in section:
                title, content = section.split(':', 1)
                title = title.strip().upper().replace(' ', '_')
                
                # Special handling for recommendations with timing and priority
                if 'RECOMMENDATIONS' in title or 'ACTION_PLAN' in title:
                    recommendations = []
                    lines = content.strip().split('\n')
                    current_rec = {}
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('- Recommendation:') or line.startswith('- Action:'):
                            if current_rec:
                                recommendations.append(current_rec)
                            current_rec = {'action': line.split(':', 1)[1].strip()}
                        elif line.startswith('- Timing:'):
                            current_rec['timing'] = line.split(':', 1)[1].strip()
                        elif line.startswith('- Priority:'):
                            current_rec['priority'] = line.split(':', 1)[1].strip()
                        elif line.startswith('- Expected Impact:'):
                            current_rec['impact'] = line.split(':', 1)[1].strip()
                    
                    if current_rec:
                        recommendations.append(current_rec)
                    
                    parsed_data[title] = recommendations
                else:
                    # Extract bullet points or numbered items for other sections
                    items = [item.strip().strip('- ').strip('* ') for item in content.strip().split('\n') if item.strip()]
                    parsed_data[title] = items

        # Create strategic plan structure
        strategic_plan = {
            "business_name": business_name,
            "business_type": business_type,
            "location": location,
            "market_analysis": {
                "target_market": target_market,
                "market_size": market_size or "To be determined",
                "market_trends": parsed_data.get("MARKET_ANALYSIS", [f"Industry-specific trends for {industry}"]),
                "analysis_text": strategic_analysis,
            },
            "competitive_positioning": {
                "unique_value_proposition": unique_value_proposition or f"Quality {business_type} services",
                "competitive_advantages": parsed_data.get("COMPETITIVE_POSITIONING", [
                    f"Specialized {business_type} expertise",
                    f"Strong market positioning in {location}",
                    "Customer-focused approach",
                ]),
                "differentiation_strategy": f"Focus on {business_type} excellence and customer experience",
            },
            "growth_strategy": {
                "short_term_goals": parsed_data.get("GROWTH_STRATEGY", growth_goals or [
                    f"Establish {business_type} market presence",
                    "Build customer base",
                    "Develop operational processes",
                ]),
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
                "market_risks": parsed_data.get("RISK_ASSESSMENT", [
                    "Economic downturn affecting customer spending",
                    "New competitors entering the market",
                    f"Industry-specific regulatory changes",
                ]),
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
            "kpis": parsed_data.get("KEY_PERFORMANCE_INDICATORS", [
                "Monthly revenue growth",
                "Customer acquisition cost",
                "Customer lifetime value",
                "Customer satisfaction score",
                f"{business_type} specific metrics",
            ]),
            "implementation_timeline": {
                "phase_1": parsed_data.get("IMPLEMENTATION_TIMELINE", ["Market research and validation", "Business setup and licensing", "Initial team hiring"]),
                "phase_2": ["Launch operations", "Marketing campaigns", "Customer acquisition"],
                "phase_3": ["Scale operations", "Process optimization", "Market expansion"],
            },
            "resource_requirements": parsed_data.get("RESOURCE_REQUIREMENTS", [
                "Initial capital investment",
                "Skilled workforce",
                "Technology infrastructure",
                "Marketing budget"
            ]),
            "key_recommendations": parsed_data.get("STRATEGIC_RECOMMENDATIONS", [
                {
                    "action": "Focus on market research and customer validation",
                    "timing": "this week",
                    "priority": "High",
                    "impact": "Validate business concept and market demand"
                },
                {
                    "action": "Develop a clear competitive advantage",
                    "timing": "next week",
                    "priority": "High", 
                    "impact": "Differentiate from competitors and establish market position"
                },
                {
                    "action": "Build strong partnerships and alliances",
                    "timing": "this month",
                    "priority": "Medium",
                    "impact": "Expand market reach and reduce operational risks"
                },
                {
                    "action": "Invest in technology and innovation",
                    "timing": "next month",
                    "priority": "Medium",
                    "impact": "Improve operational efficiency and customer experience"
                }
            ]),
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
                ],
                "analysis_text": f"Strategic analysis for {business_name} - {business_type} business (fallback response due to error: {str(e)})"
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

    BUSINESS INFORMATION:
    - Name: {business_name}
    - Type: {business_type}
    - Location: {location}
    - Target Market: {target_market}
    - Competitors: {', '.join(competitors)}
    - Unique Value Proposition: {unique_value_proposition}
    - Initial Investment: {f"${initial_investment:,.0f}" if initial_investment else "Not specified"}
    - Team Size: {f"{team_size} employees" if team_size else "Not specified"}
    - Strategic Vision: {strategic_plan.get('vision', 'Not available') if strategic_plan else 'Not available'}

    RESPONSE FORMAT - Please structure your response exactly as follows:

    STRENGTHS:
    [List 5-7 internal positive factors that give this business competitive advantages]

    WEAKNESSES:
    [Identify 4-6 internal negative factors that need to be addressed or improved]

    OPPORTUNITIES:
    [List 5-7 external positive factors that this business can capitalize on]

    THREATS:
    [Identify 4-6 external negative factors that could impact this business]

    STRATEGIC INSIGHTS:
    [Provide 3-4 key strategic insights based on the SWOT analysis]

    ACTION PLAN:
    [Outline 6-8 specific actions with timing and priority to leverage strengths, address weaknesses, capitalize on opportunities, and mitigate threats:
    - Action: [specific action]
    - Timing: [this week/next week/this month/next month]
    - Priority: [High/Medium/Low - how urgent/rush it is]
    - Expected Impact: [brief description of expected outcome]]

    Focus on providing specific, actionable insights that are highly relevant to this {business_type} business and its market position.
    """

    try:
        if OPENAI_AVAILABLE:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert business analyst specializing in SWOT analysis for {business_type} businesses. You provide detailed, actionable insights and strategic recommendations. Always respond in the exact format requested with clear sections and specific analysis.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2000,
                temperature=0.7,
            )

            swot_analysis_text = response.choices[0].message.content
        else:
            swot_analysis_text = f"SWOT analysis for {business_name} - {business_type} business"

        # Parse the AI response to extract structured data
        sections = swot_analysis_text.split('\n\n')
        parsed_data = {}
        
        for section in sections:
            if ':' in section:
                title, content = section.split(':', 1)
                title = title.strip().upper().replace(' ', '_')
                
                # Special handling for action plan with timing and priority
                if 'ACTION_PLAN' in title:
                    actions = []
                    lines = content.strip().split('\n')
                    current_action = {}
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('- Action:'):
                            if current_action:
                                actions.append(current_action)
                            current_action = {'action': line.split(':', 1)[1].strip()}
                        elif line.startswith('- Timing:'):
                            current_action['timing'] = line.split(':', 1)[1].strip()
                        elif line.startswith('- Priority:'):
                            current_action['priority'] = line.split(':', 1)[1].strip()
                        elif line.startswith('- Expected Impact:'):
                            current_action['impact'] = line.split(':', 1)[1].strip()
                    
                    if current_action:
                        actions.append(current_action)
                    
                    parsed_data[title] = actions
                else:
                    # Extract bullet points or numbered items for other sections
                    items = [item.strip().strip('- ').strip('* ') for item in content.strip().split('\n') if item.strip()]
                    parsed_data[title] = items

        return {
            "swot_analysis": {
                "strengths": parsed_data.get("STRENGTHS", [
                    "Strong business concept",
                    "Clear target market",
                    "Unique value proposition",
                    f"Specialized {business_type} expertise",
                ]),
                "weaknesses": parsed_data.get("WEAKNESSES", [
                    "Limited initial resources",
                    "New market entry",
                    "Need for brand recognition",
                    "Limited operational experience",
                ]),
                "opportunities": parsed_data.get("OPPORTUNITIES", [
                    "Growing market demand",
                    "Technology advancement",
                    "Market expansion potential",
                    "Online presence opportunities",
                ]),
                "threats": parsed_data.get("THREATS", [
                    "Competition from established players",
                    "Market volatility",
                    "Regulatory changes",
                    "Economic uncertainty",
                ]),
                "strategic_insights": parsed_data.get("STRATEGIC_INSIGHTS", [
                    "Leverage unique value proposition to differentiate from competitors",
                    "Focus on building strong customer relationships",
                    "Invest in technology to improve operational efficiency"
                ]),
                "action_plan": {
                    "immediate_actions": parsed_data.get("ACTION_PLAN", [
                        {
                            "action": "Leverage strengths to capitalize on opportunities",
                            "timing": "this week",
                            "priority": "High",
                            "impact": "Maximize competitive advantages and market opportunities"
                        },
                        {
                            "action": "Address weaknesses through strategic planning",
                            "timing": "next week",
                            "priority": "High",
                            "impact": "Improve business capabilities and reduce vulnerabilities"
                        },
                        {
                            "action": "Develop contingency plans for identified threats",
                            "timing": "this month",
                            "priority": "Medium",
                            "impact": "Prepare for potential risks and market changes"
                        },
                        {
                            "action": "Focus on building competitive advantages",
                            "timing": "next month",
                            "priority": "Medium",
                            "impact": "Strengthen market position and differentiation"
                        },
                    ]),
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
                "strategic_insights": [
                    "Leverage unique value proposition to differentiate from competitors",
                    "Focus on building strong customer relationships"
                ],
                "action_plan": {
                    "immediate_actions": [
                        "Leverage strengths to capitalize on opportunities",
                        "Address weaknesses through strategic planning",
                        "Develop contingency plans for identified threats",
                        "Focus on building competitive advantages",
                    ]
                },
                "analysis_text": f"SWOT analysis for {business_name} - {business_type} business (fallback response due to error: {str(e)})"
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

    BUSINESS INFORMATION:
    - Name: {business_name}
    - Type: {business_type}
    - Target Market: {target_market}
    - Business Model: {business_model}
    - Value Proposition: {unique_value_proposition}
    - Strategic Vision: {strategic_plan.get('vision', 'Not available') if strategic_plan else 'Not available'}
    - SWOT Strengths: {swot_analysis.get('strengths', []) if swot_analysis else 'Not available'}

    RESPONSE FORMAT - Please structure your response exactly as follows:

    KEY PARTNERS:
    [List 4-6 key partners, suppliers, and strategic alliances for this business]

    KEY ACTIVITIES:
    [Outline 5-7 core activities and processes essential for this business model]

    VALUE PROPOSITIONS:
    [Define 4-6 unique value propositions that solve customer problems and create value]

    CUSTOMER RELATIONSHIPS:
    [Describe 3-5 types of customer relationships and engagement strategies]

    CUSTOMER SEGMENTS:
    [Identify 3-5 distinct customer segments with specific characteristics and needs]

    KEY RESOURCES:
    [List 4-6 critical resources (human, physical, intellectual, financial) needed]

    CHANNELS:
    [Outline 4-6 distribution and communication channels to reach customers]

    COST STRUCTURE:
    [Break down 4-6 major cost categories and cost drivers for this business]

    REVENUE STREAMS:
    [Define 4-6 revenue sources and pricing mechanisms for this business model]

    BUSINESS MODEL INSIGHTS:
    [Provide 3-4 key insights about the business model's viability and optimization opportunities]

    RECOMMENDATIONS:
    [Suggest 5-7 specific actions to optimize and improve the business model with timing and priority:
    - Recommendation: [specific business model action]
    - Timing: [this week/next week/this month/next month]
    - Priority: [High/Medium/Low - how urgent/rush it is]
    - Expected Impact: [brief description of expected outcome]]

    Focus on creating a comprehensive, actionable Business Model Canvas that is specifically tailored to this {business_type} business and its market context.
    """

    try:
        if OPENAI_AVAILABLE:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are an expert in Business Model Canvas creation for {business_type} businesses. You provide comprehensive, actionable business model insights and strategic recommendations. Always respond in the exact format requested with clear sections and specific business model elements.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2500,
                temperature=0.7,
            )

            bmc_analysis_text = response.choices[0].message.content
        else:
            bmc_analysis_text = f"Business Model Canvas analysis for {business_name} - {business_type} business"

        # Parse the AI response to extract structured data
        sections = bmc_analysis_text.split('\n\n')
        parsed_data = {}
        
        for section in sections:
            if ':' in section:
                title, content = section.split(':', 1)
                title = title.strip().upper().replace(' ', '_')
                
                # Special handling for recommendations with timing and priority
                if 'RECOMMENDATIONS' in title:
                    recommendations = []
                    lines = content.strip().split('\n')
                    current_rec = {}
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('- Recommendation:'):
                            if current_rec:
                                recommendations.append(current_rec)
                            current_rec = {'action': line.split(':', 1)[1].strip()}
                        elif line.startswith('- Timing:'):
                            current_rec['timing'] = line.split(':', 1)[1].strip()
                        elif line.startswith('- Priority:'):
                            current_rec['priority'] = line.split(':', 1)[1].strip()
                        elif line.startswith('- Expected Impact:'):
                            current_rec['impact'] = line.split(':', 1)[1].strip()
                    
                    if current_rec:
                        recommendations.append(current_rec)
                    
                    parsed_data[title] = recommendations
                else:
                    # Extract bullet points or numbered items for other sections
                    items = [item.strip().strip('- ').strip('* ') for item in content.strip().split('\n') if item.strip()]
                    parsed_data[title] = items

        return {
            "business_model_canvas": {
                "key_partners": parsed_data.get("KEY_PARTNERS", ["Suppliers", "Technology providers", "Marketing partners", "Service providers"]),
                "key_activities": parsed_data.get("KEY_ACTIVITIES", ["Product development", "Marketing", "Customer service", "Operations management"]),
                "value_propositions": parsed_data.get("VALUE_PROPOSITIONS", ["Quality products", "Excellent service", "Competitive pricing", unique_value_proposition or f"Superior {business_type} experience"]),
                "customer_relationships": parsed_data.get("CUSTOMER_RELATIONSHIPS", ["Personal assistance", "Self-service", "Community", "Co-creation"]),
                "customer_segments": parsed_data.get("CUSTOMER_SEGMENTS", [target_market or "General market"]),
                "key_resources": parsed_data.get("KEY_RESOURCES", ["Human resources", "Technology", "Brand", "Intellectual property"]),
                "channels": parsed_data.get("CHANNELS", ["Online", "Direct sales", "Partnerships", "Social media"]),
                "cost_structure": parsed_data.get("COST_STRUCTURE", ["Operational costs", "Marketing", "Technology", "Human resources"]),
                "revenue_streams": parsed_data.get("REVENUE_STREAMS", ["Product sales", "Service fees", "Subscriptions", "Consulting"]),
                "business_model_insights": parsed_data.get("BUSINESS_MODEL_INSIGHTS", [
                    "Strong value proposition with clear customer benefits",
                    "Multiple revenue streams provide stability",
                    "Key partnerships reduce operational risks"
                ]),
                "key_insights": {
                    "recommendations": parsed_data.get("RECOMMENDATIONS", [
                        {
                            "action": "Optimize revenue streams and pricing strategy",
                            "timing": "this week",
                            "priority": "High",
                            "impact": "Improve profitability and market competitiveness"
                        },
                        {
                            "action": "Strengthen key partnerships and relationships",
                            "timing": "next week",
                            "priority": "High",
                            "impact": "Expand market reach and reduce operational risks"
                        },
                        {
                            "action": "Focus on customer acquisition and retention",
                            "timing": "this month",
                            "priority": "Medium",
                            "impact": "Build sustainable customer base and revenue growth"
                        },
                        {
                            "action": "Streamline operations to reduce costs",
                            "timing": "next month",
                            "priority": "Medium",
                            "impact": "Improve operational efficiency and profit margins"
                        },
                    ]),
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
                "business_model_insights": [
                    "Strong value proposition with clear customer benefits",
                    "Multiple revenue streams provide stability"
                ],
                "key_insights": {
                    "recommendations": [
                        "Optimize revenue streams and pricing strategy",
                        "Strengthen key partnerships and relationships",
                        "Focus on customer acquisition and retention",
                        "Streamline operations to reduce costs",
                    ],
                    "analysis_text": f"Business Model Canvas analysis for {business_name} - {business_type} business (fallback response due to error: {str(e)})"
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
    As a creative marketing expert, analyze and provide recommendations for:

    BUSINESS INFORMATION:
    - Name: {business_name}
    - Type: {business_type}
    - Target Market: {target_market}
    - Value Proposition: {unique_value_proposition}
    - Strategic Vision: {strategic_plan.get('vision', 'Not available') if strategic_plan else 'Not available'}

    RESPONSE FORMAT - Please structure your response exactly as follows:

    BRAND IDENTITY:
    [Provide 3-5 specific brand identity recommendations tailored to this business]

    MARKETING IDEAS:
    [List 5-7 creative marketing ideas specific to this business type and target market]

    UNIQUE ANGLES:
    [Provide 4-6 unique positioning angles that will help this business stand out]

    CONTENT STRATEGY:
    [Suggest 5-7 content types and strategies relevant to this business]

    VISUAL CONCEPTS:
    [Recommend 4-6 visual identity concepts including colors, styles, and design elements]

    CAMPAIGN IDEAS:
    [Propose 4-6 specific marketing campaign ideas with brief descriptions]

    KEY RECOMMENDATIONS:
    [Provide 5-7 actionable creative recommendations with timing and priority:
    - Recommendation: [specific creative action]
    - Timing: [this week/next week/this month/next month]
    - Priority: [High/Medium/Low - how urgent/rush it is]
    - Expected Impact: [brief description of expected outcome]]

    CREATIVE INSIGHTS:
    [Share 2-3 unique creative insights or innovative approaches for this specific business]

    Focus on being highly specific to this {business_type} business and its target market. Make each recommendation actionable and tailored to their unique value proposition.
    """

    try:
        if OPENAI_AVAILABLE:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a creative marketing expert specializing in {business_type} businesses. You provide innovative, specific, and actionable creative solutions. Always respond in the exact format requested with clear sections and bullet points.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2000,
                temperature=0.8,
            )

            creative_analysis_text = response.choices[0].message.content
        else:
            creative_analysis_text = f"Creative analysis for {business_name} - {business_type} business"

        # Parse the AI response to extract structured data
        sections = creative_analysis_text.split('\n\n')
        parsed_data = {}
        
        for section in sections:
            if ':' in section:
                title, content = section.split(':', 1)
                title = title.strip().upper().replace(' ', '_')
                
                # Special handling for recommendations with timing and priority
                if 'KEY_RECOMMENDATIONS' in title:
                    recommendations = []
                    lines = content.strip().split('\n')
                    current_rec = {}
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('- Recommendation:'):
                            if current_rec:
                                recommendations.append(current_rec)
                            current_rec = {'action': line.split(':', 1)[1].strip()}
                        elif line.startswith('- Timing:'):
                            current_rec['timing'] = line.split(':', 1)[1].strip()
                        elif line.startswith('- Priority:'):
                            current_rec['priority'] = line.split(':', 1)[1].strip()
                        elif line.startswith('- Expected Impact:'):
                            current_rec['impact'] = line.split(':', 1)[1].strip()
                    
                    if current_rec:
                        recommendations.append(current_rec)
                    
                    parsed_data[title] = recommendations
                else:
                    # Extract bullet points or numbered items for other sections
                    items = [item.strip().strip('- ').strip('* ') for item in content.strip().split('\n') if item.strip()]
                    parsed_data[title] = items

        return {
            "creative_analysis": {
                "brand_identity": parsed_data.get("BRAND_IDENTITY", [f"Modern, innovative {business_type}"]),
                "marketing_ideas": parsed_data.get("MARKETING_IDEAS", ["Social media campaigns", "Influencer partnerships", "Content marketing"]),
                "unique_angles": parsed_data.get("UNIQUE_ANGLES", ["Customer-centric approach", "Technology integration", "Sustainability focus"]),
                "content_strategy": parsed_data.get("CONTENT_STRATEGY", ["Educational content", "Behind-the-scenes content", "Customer testimonials"]),
                "visual_concepts": parsed_data.get("VISUAL_CONCEPTS", ["Modern, clean design", "Bold color palette", "Professional photography"]),
                "campaign_ideas": parsed_data.get("CAMPAIGN_IDEAS", ["Launch campaign", "Seasonal promotions", "Referral programs"]),
                "recommendations": parsed_data.get("KEY_RECOMMENDATIONS", [
                    {
                        "action": "Develop a strong, memorable brand identity",
                        "timing": "this week",
                        "priority": "High",
                        "impact": "Establish brand recognition and market differentiation"
                    },
                    {
                        "action": "Create engaging content marketing strategies",
                        "timing": "next week",
                        "priority": "High",
                        "impact": "Build customer engagement and drive traffic"
                    },
                    {
                        "action": "Leverage social media and digital platforms",
                        "timing": "this month",
                        "priority": "Medium",
                        "impact": "Expand reach and connect with target audience"
                    },
                    {
                        "action": "Focus on customer experience and satisfaction",
                        "timing": "next month",
                        "priority": "Medium",
                        "impact": "Build customer loyalty and positive word-of-mouth"
                    },
                    {
                        "action": "Build community and engagement",
                        "timing": "next month",
                        "priority": "Low",
                        "impact": "Create loyal customer base and brand advocates"
                    }
                ]),
                "creative_insights": parsed_data.get("CREATIVE_INSIGHTS", [
                    "Leverage technology to create unique customer experiences",
                    "Focus on building emotional connections with target audience"
                ]),
                "analysis_text": creative_analysis_text,
            }
        }

    except Exception as e:
        print(f"Error in creative analysis: {e}")
        return {
            "creative_analysis": {
                "brand_identity": [f"Modern, innovative {business_type}"],
                "marketing_ideas": ["Social media campaigns", "Influencer partnerships", "Content marketing"],
                "unique_angles": ["Customer-centric approach", "Technology integration", "Sustainability focus"],
                "content_strategy": ["Educational content", "Behind-the-scenes content", "Customer testimonials"],
                "visual_concepts": ["Modern, clean design", "Bold color palette", "Professional photography"],
                "campaign_ideas": ["Launch campaign", "Seasonal promotions", "Referral programs"],
                "recommendations": [
                    "Develop a strong, memorable brand identity",
                    "Create engaging content marketing strategies",
                    "Leverage social media and digital platforms",
                    "Focus on customer experience and satisfaction",
                    "Build community and engagement"
                ],
                "creative_insights": [
                    "Leverage technology to create unique customer experiences",
                    "Focus on building emotional connections with target audience"
                ],
                "analysis_text": f"Creative analysis for {business_name} - {business_type} business (fallback response due to error: {str(e)})"
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

    BUSINESS INFORMATION:
    - Name: {business_name}
    - Type: {business_type}
    - Initial Investment: {f"${initial_investment:,.0f}" if initial_investment else "Not specified"}
    - Team Size: {f"{team_size} employees" if team_size else "Not specified"}
    - Strategic Vision: {strategic_plan.get('vision', 'Not available') if strategic_plan else 'Not available'}

    RESPONSE FORMAT - Please structure your response exactly as follows:

    FINANCIAL PROJECTIONS:
    [Provide 3-5 year financial projections with specific revenue, expense, and profit estimates]

    BREAK-EVEN ANALYSIS:
    [Calculate and explain break-even timeline and requirements for this specific business]

    FUNDING RECOMMENDATIONS:
    [List 5-7 funding sources and strategies appropriate for this business type and size]

    COST STRUCTURE:
    [Break down fixed and variable costs specific to this {business_type} business]

    REVENUE MODEL:
    [Suggest 4-6 revenue streams and pricing strategies for this business]

    FINANCIAL RISKS:
    [Identify 4-6 key financial risks and mitigation strategies]

    KEY METRICS:
    [Define 5-7 important financial KPIs to track for this business]

    ACTIONABLE RECOMMENDATIONS:
    [Provide 6-8 specific, actionable financial recommendations with timing and priority:
    - Recommendation: [specific financial action]
    - Timing: [this week/next week/this month/next month]
    - Priority: [High/Medium/Low - how urgent/rush it is]
    - Expected Impact: [brief description of expected outcome]]

    Focus on practical, realistic financial advice tailored to this {business_type} business and its specific circumstances.
    """

    try:
        if OPENAI_AVAILABLE:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a financial analyst specializing in {business_type} businesses. You provide practical, actionable financial advice and realistic projections. Always respond in the exact format requested with clear sections and specific numbers where possible.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2000,
                temperature=0.7,
            )

            financial_analysis_text = response.choices[0].message.content
        else:
            financial_analysis_text = f"Financial analysis for {business_name} - {business_type} business"

        # Parse the AI response to extract structured data
        sections = financial_analysis_text.split('\n\n')
        parsed_data = {}
        
        for section in sections:
            if ':' in section:
                title, content = section.split(':', 1)
                title = title.strip().upper().replace(' ', '_')
                
                # Special handling for recommendations with timing and priority
                if 'ACTIONABLE_RECOMMENDATIONS' in title:
                    recommendations = []
                    lines = content.strip().split('\n')
                    current_rec = {}
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('- Recommendation:'):
                            if current_rec:
                                recommendations.append(current_rec)
                            current_rec = {'action': line.split(':', 1)[1].strip()}
                        elif line.startswith('- Timing:'):
                            current_rec['timing'] = line.split(':', 1)[1].strip()
                        elif line.startswith('- Priority:'):
                            current_rec['priority'] = line.split(':', 1)[1].strip()
                        elif line.startswith('- Expected Impact:'):
                            current_rec['impact'] = line.split(':', 1)[1].strip()
                    
                    if current_rec:
                        recommendations.append(current_rec)
                    
                    parsed_data[title] = recommendations
                else:
                    # Extract bullet points or numbered items for other sections
                    items = [item.strip().strip('- ').strip('* ') for item in content.strip().split('\n') if item.strip()]
                    parsed_data[title] = items

        return {
            "financial_analysis": {
                "startup_costs": initial_investment or 50000,
                "projected_revenue": parsed_data.get("FINANCIAL_PROJECTIONS", ["To be determined based on market analysis"]),
                "break_even_analysis": parsed_data.get("BREAK-EVEN_ANALYSIS", ["6-12 months projected"]),
                "funding_recommendations": parsed_data.get("FUNDING_RECOMMENDATIONS", [
                    "Bootstrap initially",
                    "Seek angel investment",
                    "Consider crowdfunding",
                    "Explore small business loans",
                ]),
                "cost_structure": {
                    "fixed_costs": parsed_data.get("COST_STRUCTURE", ["Rent", "Utilities", "Insurance", "Software subscriptions"]),
                    "variable_costs": ["Materials", "Labor", "Marketing", "Commissions"],
                },
                "revenue_model": {
                    "primary_streams": parsed_data.get("REVENUE_MODEL", ["Product sales", "Service fees"]),
                    "secondary_streams": ["Consulting", "Training", "Licensing"],
                },
                "financial_risks": parsed_data.get("FINANCIAL_RISKS", [
                    "Market volatility",
                    "Cash flow challenges",
                    "Unexpected expenses",
                    "Competition pressure"
                ]),
                "key_metrics": parsed_data.get("KEY_METRICS", [
                    "Monthly Recurring Revenue (MRR)",
                    "Customer Acquisition Cost (CAC)",
                    "Lifetime Value (LTV)",
                    "Burn Rate",
                    "Profit Margins"
                ]),
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
                "recommendations": parsed_data.get("ACTIONABLE_RECOMMENDATIONS", [
                    {
                        "action": "Maintain strict financial discipline and budgeting",
                        "timing": "this week",
                        "priority": "High",
                        "impact": "Ensure financial stability and prevent cash flow issues"
                    },
                    {
                        "action": "Diversify funding sources and revenue streams",
                        "timing": "next week",
                        "priority": "High",
                        "impact": "Reduce financial risk and increase revenue potential"
                    },
                    {
                        "action": "Monitor cash flow and financial metrics closely",
                        "timing": "this month",
                        "priority": "Medium",
                        "impact": "Identify financial trends and make informed decisions"
                    },
                    {
                        "action": "Plan for scalability and growth investments",
                        "timing": "next month",
                        "priority": "Medium",
                        "impact": "Prepare for business expansion and increased capacity"
                    },
                    {
                        "action": "Build emergency fund for unexpected expenses",
                        "timing": "next month",
                        "priority": "Low",
                        "impact": "Provide financial security and risk mitigation"
                    },
                ]),
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
                "financial_risks": [
                    "Market volatility",
                    "Cash flow challenges",
                    "Unexpected expenses",
                    "Competition pressure"
                ],
                "key_metrics": [
                    "Monthly Recurring Revenue (MRR)",
                    "Customer Acquisition Cost (CAC)",
                    "Lifetime Value (LTV)",
                    "Burn Rate",
                    "Profit Margins"
                ],
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
                "analysis_text": f"Financial analysis for {business_name} - {business_type} business (fallback response due to error: {str(e)})",
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

    BUSINESS INFORMATION:
    - Name: {business_name}
    - Type: {business_type}
    - Target Market: {target_market}
    - Business Model: {business_model}
    - Strategic Vision: {strategic_plan.get('vision', 'Not available') if strategic_plan else 'Not available'}

    RESPONSE FORMAT - Please structure your response exactly as follows:

    SALES STRATEGY:
    [Provide 4-6 core sales strategies specific to this {business_type} business]

    TARGET CUSTOMERS:
    [Define 3-5 specific customer segments with detailed characteristics]

    SALES CHANNELS:
    [List 5-7 effective sales channels and methods for this business]

    PRICING STRATEGY:
    [Suggest 3-4 pricing approaches and strategies for this business model]

    SALES PROCESS:
    [Outline 6-8 step sales process tailored to this business type]

    LEAD GENERATION:
    [Provide 5-7 lead generation strategies specific to this target market]

    CUSTOMER ACQUISITION:
    [Suggest 5-7 customer acquisition tactics for this business]

    SALES TEAM STRUCTURE:
    [Recommend team structure, roles, and training for this business size]

    KEY RECOMMENDATIONS:
    [Provide 6-8 actionable sales recommendations with timing and priority:
    - Recommendation: [specific sales action]
    - Timing: [this week/next week/this month/next month]
    - Priority: [High/Medium/Low - how urgent/rush it is]
    - Expected Impact: [brief description of expected outcome]]

    Focus on practical, effective sales strategies that will drive revenue growth for this specific {business_type} business.
    """

    try:
        if OPENAI_AVAILABLE:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a sales strategy expert specializing in {business_type} businesses. You provide practical, effective sales strategies and actionable tactics. Always respond in the exact format requested with clear sections and specific strategies.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2000,
                temperature=0.7,
            )

            sales_analysis_text = response.choices[0].message.content
        else:
            sales_analysis_text = f"Sales analysis for {business_name} - {business_type} business"

        # Parse the AI response to extract structured data
        sections = sales_analysis_text.split('\n\n')
        parsed_data = {}
        
        for section in sections:
            if ':' in section:
                title, content = section.split(':', 1)
                title = title.strip().upper().replace(' ', '_')
                
                # Special handling for recommendations with timing and priority
                if 'KEY_RECOMMENDATIONS' in title:
                    recommendations = []
                    lines = content.strip().split('\n')
                    current_rec = {}
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('- Recommendation:'):
                            if current_rec:
                                recommendations.append(current_rec)
                            current_rec = {'action': line.split(':', 1)[1].strip()}
                        elif line.startswith('- Timing:'):
                            current_rec['timing'] = line.split(':', 1)[1].strip()
                        elif line.startswith('- Priority:'):
                            current_rec['priority'] = line.split(':', 1)[1].strip()
                        elif line.startswith('- Expected Impact:'):
                            current_rec['impact'] = line.split(':', 1)[1].strip()
                    
                    if current_rec:
                        recommendations.append(current_rec)
                    
                    parsed_data[title] = recommendations
                else:
                    # Extract bullet points or numbered items for other sections
                    items = [item.strip().strip('- ').strip('* ') for item in content.strip().split('\n') if item.strip()]
                    parsed_data[title] = items

        return {
            "sales_strategy": {
                "target_customers": parsed_data.get("TARGET_CUSTOMERS", [target_market or "General market"]),
                "sales_channels": parsed_data.get("SALES_CHANNELS", [
                    "Direct sales",
                    "Online platform",
                    "Partnerships",
                    "Social media",
                    "Referrals",
                ]),
                "pricing_strategy": parsed_data.get("PRICING_STRATEGY", ["Competitive pricing with value-based options"]),
                "sales_process": parsed_data.get("SALES_PROCESS", [
                    "Lead generation",
                    "Qualification",
                    "Presentation",
                    "Closing",
                    "Follow-up",
                ]),
                "lead_generation": parsed_data.get("LEAD_GENERATION", [
                    "Content marketing",
                    "Social media advertising",
                    "Networking events",
                    "Referral programs",
                    "Cold outreach",
                ]),
                "customer_acquisition": parsed_data.get("CUSTOMER_ACQUISITION", [
                    "Free trials",
                    "Discounts for early adopters",
                    "Referral incentives",
                    "Partnership marketing",
                    "Content marketing",
                ]),
                "sales_team": {
                    "structure": parsed_data.get("SALES_TEAM_STRUCTURE", ["Small, focused team"]),
                    "training": ["Product knowledge", "Sales techniques", "Customer service"],
                    "incentives": ["Commission-based", "Performance bonuses", "Career growth"],
                },
                "recommendations": parsed_data.get("KEY_RECOMMENDATIONS", [
                    {
                        "action": "Develop a comprehensive sales strategy and process",
                        "timing": "this week",
                        "priority": "High",
                        "impact": "Establish systematic approach to sales and customer acquisition"
                    },
                    {
                        "action": "Build strong relationships with target customers",
                        "timing": "next week",
                        "priority": "High",
                        "impact": "Increase customer loyalty and repeat business"
                    },
                    {
                        "action": "Implement effective lead generation and qualification",
                        "timing": "this month",
                        "priority": "Medium",
                        "impact": "Improve sales pipeline quality and conversion rates"
                    },
                    {
                        "action": "Focus on value-based selling and customer success",
                        "timing": "next month",
                        "priority": "Medium",
                        "impact": "Differentiate from competitors and increase customer satisfaction"
                    },
                    {
                        "action": "Invest in sales team training and development",
                        "timing": "next month",
                        "priority": "Low",
                        "impact": "Improve sales performance and team capabilities"
                    },
                ]),
                "analysis_text": sales_analysis_text,
            }
        }

    except Exception as e:
        print(f"Error in sales analysis: {e}")
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
                "analysis_text": f"Sales analysis for {business_name} - {business_type} business (fallback response due to error: {str(e)})",
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

    BUSINESS INFORMATION:
    - Name: {business_name}
    - Type: {business_type}
    - Market Size: {market_size}
    - Competitors: {', '.join(competitors)}

    INTEGRATED ANALYSIS DATA:
    - Strategic Vision: {strategic_insights.get('vision', 'Not available')}
    - Creative Brand Identity: {creative_insights.get('brand_identity', 'Not available')}
    - Financial Startup Costs: {financial_insights.get('startup_costs', 'Not available')}
    - Sales Target Customers: {sales_insights.get('target_customers', 'Not available')}
    - SWOT Strengths: {swot_insights.get('strengths', 'Not available')}
    - Business Model Partners: {bmc_insights.get('key_partners', 'Not available')}

    RESPONSE FORMAT - Please structure your response exactly as follows:

    MARKET ANALYSIS:
    [Provide 4-6 comprehensive market insights including size, trends, and growth potential]

    COMPETITIVE LANDSCAPE:
    [Analyze 4-6 competitive factors and positioning opportunities for this business]

    SUCCESS PROBABILITY:
    [Assess 4-5 factors that influence the business success probability with specific percentages]

    KEY PERFORMANCE INDICATORS:
    [Define 5-7 critical KPIs that should be tracked for this business type]

    DATA-DRIVEN INSIGHTS:
    [Provide 4-6 actionable insights based on the integrated analysis of all agent data]

    RISK ASSESSMENT:
    [Identify 4-6 key risks and data-driven mitigation strategies]

    GROWTH OPPORTUNITIES:
    [Outline 4-6 specific growth opportunities with supporting data insights]

    ANALYTICS RECOMMENDATIONS:
    [Provide 6-8 data-driven recommendations with timing and priority:
    - Recommendation: [specific action]
    - Timing: [this week/next week/this month/next month]
    - Priority: [High/Medium/Low - how urgent/rush it is]
    - Expected Impact: [brief description of expected outcome]]

    Synthesize all the information from different analyses to provide actionable, data-driven insights for this {business_type} business.
    """

    try:
        if OPENAI_AVAILABLE:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a business analytics expert specializing in {business_type} businesses. You synthesize multiple analyses to provide comprehensive, data-driven insights and actionable recommendations. Always respond in the exact format requested with clear sections and specific analytics insights.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2500,
                temperature=0.7,
            )

            analytics_analysis_text = response.choices[0].message.content
        else:
            analytics_analysis_text = f"Analytics analysis for {business_name} - {business_type} business"

        # Parse the AI response to extract structured data
        sections = analytics_analysis_text.split('\n\n')
        parsed_data = {}
        
        for section in sections:
            if ':' in section:
                title, content = section.split(':', 1)
                title = title.strip().upper().replace(' ', '_')
                
                # Special handling for recommendations with timing and priority
                if 'ANALYTICS_RECOMMENDATIONS' in title:
                    recommendations = []
                    lines = content.strip().split('\n')
                    current_rec = {}
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('- Recommendation:'):
                            if current_rec:
                                recommendations.append(current_rec)
                            current_rec = {'action': line.split(':', 1)[1].strip()}
                        elif line.startswith('- Timing:'):
                            current_rec['timing'] = line.split(':', 1)[1].strip()
                        elif line.startswith('- Priority:'):
                            current_rec['priority'] = line.split(':', 1)[1].strip()
                        elif line.startswith('- Expected Impact:'):
                            current_rec['impact'] = line.split(':', 1)[1].strip()
                    
                    if current_rec:
                        recommendations.append(current_rec)
                    
                    parsed_data[title] = recommendations
                else:
                    # Extract bullet points or numbered items for other sections
                    items = [item.strip().strip('- ').strip('* ') for item in content.strip().split('\n') if item.strip()]
                    parsed_data[title] = items

        return {
            "analytics_summary": {
                "market_size": market_size or "To be analyzed",
                "competition_level": "Moderate to high",
                "success_probability": {
                    "overall_success_rate": "70%",
                    "market_conditions": "Favorable",
                    "competitive_advantage": "Strong",
                    "execution_risk": "Medium",
                },
                "key_metrics": parsed_data.get("KEY_PERFORMANCE_INDICATORS", [
                    "Customer acquisition cost",
                    "Lifetime value",
                    "Conversion rate",
                    "Customer satisfaction score",
                    "Revenue growth rate",
                ]),
                "competitive_analysis": parsed_data.get("COMPETITIVE_LANDSCAPE", [f"Analysis of {len(competitors)} competitors in the {business_type} market"]),
                "data_insights": parsed_data.get("DATA-DRIVEN_INSIGHTS", [
                    "Strong market opportunity",
                    "Clear competitive positioning",
                    "Solid financial foundation",
                    "Effective sales strategy",
                ]),
                "risk_assessment": parsed_data.get("RISK_ASSESSMENT", [
                    "Market volatility risk",
                    "Competition intensity",
                    "Execution challenges",
                    "Resource constraints"
                ]),
                "growth_opportunities": parsed_data.get("GROWTH_OPPORTUNITIES", [
                    "Market expansion potential",
                    "Technology integration opportunities",
                    "Partnership development",
                    "Product diversification"
                ]),
                "recommendations": parsed_data.get("ANALYTICS_RECOMMENDATIONS", [
                    {
                        "action": "Track and analyze key performance metrics",
                        "timing": "this week",
                        "priority": "High",
                        "impact": "Establish data-driven decision making foundation"
                    },
                    {
                        "action": "Use data-driven insights for decision making",
                        "timing": "next week",
                        "priority": "High",
                        "impact": "Improve business decisions and strategic planning"
                    },
                    {
                        "action": "Monitor market trends and competitive landscape",
                        "timing": "this month",
                        "priority": "Medium",
                        "impact": "Stay ahead of market changes and competitive threats"
                    },
                    {
                        "action": "Continuously optimize based on performance data",
                        "timing": "next month",
                        "priority": "Medium",
                        "impact": "Improve operational efficiency and customer satisfaction"
                    },
                    {
                        "action": "Implement A/B testing for optimization",
                        "timing": "next month",
                        "priority": "Low",
                        "impact": "Systematically improve conversion rates and user experience"
                    },
                ]),
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
                "data_insights": [
                    "Strong market opportunity",
                    "Clear competitive positioning",
                    "Solid financial foundation"
                ],
                "risk_assessment": [
                    "Market volatility risk",
                    "Competition intensity",
                    "Execution challenges"
                ],
                "growth_opportunities": [
                    "Market expansion potential",
                    "Technology integration opportunities",
                    "Partnership development"
                ],
                "recommendations": [
                    {
                        "action": "Track and analyze key performance metrics",
                        "timing": "this week",
                        "priority": "High",
                        "impact": "Establish data-driven decision making foundation"
                    },
                    {
                        "action": "Use data-driven insights for decision making",
                        "timing": "next week",
                        "priority": "High",
                        "impact": "Improve business decisions and strategic planning"
                    },
                    {
                        "action": "Monitor market trends and competitive landscape",
                        "timing": "this month",
                        "priority": "Medium",
                        "impact": "Stay ahead of market changes and competitive threats"
                    },
                    {
                        "action": "Continuously optimize based on performance data",
                        "timing": "next month",
                        "priority": "Medium",
                        "impact": "Improve operational efficiency and customer satisfaction"
                    }
                ],
                "analysis_text": f"Analytics analysis for {business_name} - {business_type} business (fallback response due to error: {str(e)})"
            }
        }


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
        if OPENAI_AVAILABLE:
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
        else:
            task_assignment_text = f"Task assignment for {business_name} - {business_type} business"

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
                "Set up performance tracking system",
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
                "Optimize revenue model",
                "Develop partnership strategy",
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

    BUSINESS INFORMATION:
    - Name: {business_name}
    - Type: {business_type}
    - Team Size: {f"{team_size} employees" if team_size else "Not specified"}
    - Target Market: {target_market}
    - Value Proposition: {unique_value_proposition}
    - Growth Goals: {', '.join(growth_goals)}

    INTEGRATED AGENT ANALYSIS:
    - Strategic Vision: {strategic_plan.get('vision', 'Not available')}
    - Creative Brand Identity: {creative_analysis.get('brand_identity', 'Not available')}
    - Financial Startup Costs: {financial_analysis.get('startup_costs', 'Not available')}
    - Sales Target Customers: {sales_strategy.get('target_customers', 'Not available')}
    - SWOT Strengths: {swot_analysis.get('strengths', 'Not available')}
    - Business Model Partners: {bmc_analysis.get('key_partners', 'Not available')}
    - Analytics Market Size: {analytics_summary.get('market_size', 'Not available')}

    RESPONSE FORMAT - Please structure your response exactly as follows:

    OPERATIONAL PRIORITIES:
    [List 4-6 top operational priorities for this business based on the integrated analysis]

    STRATEGIC AGENT TASKS:
    [Provide 4-6 specific, actionable tasks for strategic planning and market analysis]

    CREATIVE AGENT TASKS:
    [Outline 4-6 creative tasks for brand development and marketing content]

    FINANCIAL AGENT TASKS:
    [Define 4-6 financial tasks for planning, budgeting, and cost optimization]

    SALES AGENT TASKS:
    [Specify 4-6 sales tasks for customer acquisition and revenue generation]

    ANALYTICS AGENT TASKS:
    [Detail 4-6 analytics tasks for performance tracking and data insights]

    TEAM MANAGEMENT:
    [Provide 3-4 team management recommendations for this business size]

    PROJECT TIMELINE:
    [Outline 4-5 key milestones and timeline for task execution]

    SUCCESS METRICS:
    [Define 4-5 key metrics to measure task completion and business success]

    MANAGEMENT RECOMMENDATIONS:
    [Provide 5-7 actionable management recommendations with timing and priority:
    - Recommendation: [specific management action]
    - Timing: [this week/next week/this month/next month]
    - Priority: [High/Medium/Low - how urgent/rush it is]
    - Expected Impact: [brief description of expected outcome]]

    Focus on creating specific, actionable tasks that leverage the strengths identified in the SWOT analysis and align with the strategic vision for this {business_type} business.
    """

    try:
        if OPENAI_AVAILABLE:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": f"You are a senior business manager and project coordinator specializing in {business_type} businesses. You create comprehensive, actionable task assignments and operational plans. Always respond in the exact format requested with clear sections and specific task details.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=2500,
                temperature=0.7,
            )

            manager_analysis_text = response.choices[0].message.content
        else:
            manager_analysis_text = f"Manager analysis for {business_name} - {business_type} business"

        # Parse the AI response to extract structured data
        sections = manager_analysis_text.split('\n\n')
        parsed_data = {}
        
        for section in sections:
            if ':' in section:
                title, content = section.split(':', 1)
                title = title.strip().upper().replace(' ', '_')
                
                # Special handling for recommendations with timing and priority
                if 'MANAGEMENT_RECOMMENDATIONS' in title:
                    recommendations = []
                    lines = content.strip().split('\n')
                    current_rec = {}
                    
                    for line in lines:
                        line = line.strip()
                        if line.startswith('- Recommendation:'):
                            if current_rec:
                                recommendations.append(current_rec)
                            current_rec = {'action': line.split(':', 1)[1].strip()}
                        elif line.startswith('- Timing:'):
                            current_rec['timing'] = line.split(':', 1)[1].strip()
                        elif line.startswith('- Priority:'):
                            current_rec['priority'] = line.split(':', 1)[1].strip()
                        elif line.startswith('- Expected Impact:'):
                            current_rec['impact'] = line.split(':', 1)[1].strip()
                    
                    if current_rec:
                        recommendations.append(current_rec)
                    
                    parsed_data[title] = recommendations
                else:
                    # Extract bullet points or numbered items for other sections
                    items = [item.strip().strip('- ').strip('* ') for item in content.strip().split('\n') if item.strip()]
                    parsed_data[title] = items

        # Generate dynamic tasks based on parsed data
        dynamic_tasks = _generate_dynamic_tasks(business_data, all_agent_data)

        return {
            "manager_analysis": {
                "operational_priorities": parsed_data.get("OPERATIONAL_PRIORITIES", [
                    "Establish operational processes",
                    "Build team capabilities",
                    "Implement tracking systems",
                    "Optimize resource allocation"
                ]),
                "agent_tasks": {
                    "strategic_agent": parsed_data.get("STRATEGIC_AGENT_TASKS", [
                        "Conduct market research and competitive analysis",
                        "Develop strategic plan and goal setting",
                        "Optimize business model",
                        "Create implementation timeline"
                    ]),
                    "creative_agent": parsed_data.get("CREATIVE_AGENT_TASKS", [
                        "Develop brand identity and guidelines",
                        "Create marketing content and materials",
                        "Design visual assets and templates",
                        "Plan creative campaigns"
                    ]),
                    "financial_agent": parsed_data.get("FINANCIAL_AGENT_TASKS", [
                        "Create financial projections and budgets",
                        "Analyze cost structure and optimization",
                        "Develop funding strategy",
                        "Set up financial tracking systems"
                    ]),
                    "sales_agent": parsed_data.get("SALES_AGENT_TASKS", [
                        "Develop sales strategy and process",
                        "Create customer acquisition campaigns",
                        "Optimize sales pipeline",
                        "Train sales team"
                    ]),
                    "analytics_agent": parsed_data.get("ANALYTICS_AGENT_TASKS", [
                        "Set up performance tracking systems",
                        "Create data analysis dashboards",
                        "Develop customer insights programs",
                        "Monitor competitive landscape",
                    ]),
                },
                "team_management": parsed_data.get("TEAM_MANAGEMENT", [
                    "Establish clear roles and responsibilities",
                    "Implement communication protocols",
                    "Create performance evaluation systems",
                    "Develop training programs"
                ]),
                "project_timeline": parsed_data.get("PROJECT_TIMELINE", [
                    "Phase 1: Foundation (0-3 months)",
                    "Phase 2: Launch (3-6 months)",
                    "Phase 3: Growth (6-12 months)",
                    "Phase 4: Optimization (12+ months)"
                ]),
                "success_metrics": parsed_data.get("SUCCESS_METRICS", [
                    "Task completion rate",
                    "Project milestone achievement",
                    "Team productivity metrics",
                    "Business performance indicators"
                ]),
                "recommendations": parsed_data.get("MANAGEMENT_RECOMMENDATIONS", [
                    {
                        "action": "Implement agile project management methodology",
                        "timing": "this week",
                        "priority": "High",
                        "impact": "Improve project delivery and team coordination"
                    },
                    {
                        "action": "Establish regular team meetings and check-ins",
                        "timing": "next week",
                        "priority": "High",
                        "impact": "Enhance communication and accountability"
                    },
                    {
                        "action": "Use data-driven decision making",
                        "timing": "this month",
                        "priority": "Medium",
                        "impact": "Improve decision quality and business outcomes"
                    },
                    {
                        "action": "Focus on continuous improvement",
                        "timing": "next month",
                        "priority": "Medium",
                        "impact": "Build learning culture and operational excellence"
                    },
                    {
                        "action": "Build strong team culture and communication",
                        "timing": "next month",
                        "priority": "Low",
                        "impact": "Improve team morale and retention"
                    },
                ]),
                "dynamic_tasks": dynamic_tasks,
                "analysis_text": manager_analysis_text,
            }
        }

    except Exception as e:
        print(f"Error in manager analysis: {e}")
        return {
            "manager_analysis": {
                "operational_priorities": [
                    "Establish operational processes",
                    "Build team capabilities",
                    "Implement tracking systems"
                ],
                "agent_tasks": {
                    "strategic_agent": ["Conduct market research", "Develop strategic plan"],
                    "creative_agent": ["Develop brand identity", "Create marketing content"],
                    "financial_agent": ["Create financial projections", "Analyze cost structure"],
                    "sales_agent": ["Develop sales strategy", "Create acquisition campaigns"],
                    "analytics_agent": ["Set up tracking systems", "Analyze data insights"],
                },
                "team_management": [
                    "Establish clear roles and responsibilities",
                    "Implement communication protocols"
                ],
                "project_timeline": [
                    "Phase 1: Foundation (0-3 months)",
                    "Phase 2: Launch (3-6 months)",
                    "Phase 3: Growth (6-12 months)"
                ],
                "success_metrics": [
                    "Task completion rate",
                    "Project milestone achievement",
                    "Team productivity metrics"
                ],
                "recommendations": [
                    {
                        "action": "Implement agile project management methodology",
                        "timing": "this week",
                        "priority": "High",
                        "impact": "Improve project delivery and team coordination"
                    },
                    {
                        "action": "Establish regular team meetings and check-ins",
                        "timing": "next week",
                        "priority": "High",
                        "impact": "Enhance communication and accountability"
                    },
                    {
                        "action": "Use data-driven decision making",
                        "timing": "this month",
                        "priority": "Medium",
                        "impact": "Improve decision quality and business outcomes"
                    },
                    {
                        "action": "Focus on continuous improvement",
                        "timing": "next month",
                        "priority": "Medium",
                        "impact": "Build learning culture and operational excellence"
                    }
                ],
                "analysis_text": f"Manager analysis for {business_name} - {business_type} business (fallback response due to error: {str(e)})",
            }
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
            "expected_outcome": "Grand opening campaign and customer acquisition"
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