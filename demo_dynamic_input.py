#!/usr/bin/env python3
"""
Demonstration script for dynamic business input system
Shows how to use the system with different business types
"""

import asyncio
import httpx
import json
from datetime import datetime

# Core agent URL
CORE_AGENT_URL = "http://localhost:5099"

# Example business data for different types
BUSINESS_EXAMPLES = {
    "coffee_shop": {
        "business_name": "ร้านกาแฟสดใจดี",
        "business_type": "coffee_shop",
        "location": "กรุงเทพมหานคร",
        "description": "A premium coffee shop offering high-quality coffee and pastries in a welcoming atmosphere",
        "target_market": "Young professionals and students aged 20-35 who appreciate quality coffee and community atmosphere",
        "competitors": ["ร้านกาแฟ Amazon", "ร้านกาแฟ All Cafe", "Starbucks"],
        "growth_goals": ["เพิ่มยอดขาย 50% ภายใน 1 ปี", "ขยายสาขาใหม่ 2 สาขา", "เปิดบริการส่ง"],
        "initial_investment": 50000.0,
        "team_size": 8,
        "unique_value_proposition": "Authentic Thai coffee experience with community focus",
        "business_model": "b2c",
        "industry": "food_beverage",
        "market_size": "local",
        "technology_requirements": [
            "POS system",
            "Inventory management",
            "Online ordering",
        ],
        "regulatory_requirements": ["Food safety license", "Business registration"],
    },
    "tech_startup": {
        "business_name": "TechFlow Solutions",
        "business_type": "tech_startup",
        "location": "San Francisco, CA",
        "description": "AI-powered workflow automation platform for small businesses",
        "target_market": "Small to medium businesses (10-500 employees) looking to automate repetitive tasks",
        "competitors": ["Zapier", "Microsoft Power Automate", "Automation Anywhere"],
        "growth_goals": [
            "Reach 1000 customers in 12 months",
            "Expand to European market",
            "Launch mobile app",
        ],
        "initial_investment": 200000.0,
        "team_size": 15,
        "unique_value_proposition": "No-code AI automation specifically designed for small businesses",
        "business_model": "b2b",
        "industry": "technology",
        "market_size": "national",
        "technology_requirements": [
            "Cloud infrastructure",
            "AI/ML platform",
            "Mobile app development",
        ],
        "regulatory_requirements": [
            "Data protection compliance",
            "SOC 2 certification",
        ],
    },
    "restaurant": {
        "business_name": "Fusion Bistro",
        "business_type": "restaurant",
        "location": "New York, NY",
        "description": "Modern fusion restaurant combining Asian and European cuisines",
        "target_market": "Food enthusiasts aged 25-45 with disposable income, seeking unique dining experiences",
        "competitors": ["Momofuku", "Eleven Madison Park", "Le Bernardin"],
        "growth_goals": [
            "Achieve Michelin star recognition",
            "Open second location",
            "Launch catering service",
        ],
        "initial_investment": 300000.0,
        "team_size": 25,
        "unique_value_proposition": "Innovative fusion cuisine with seasonal ingredients and artistic presentation",
        "business_model": "b2c",
        "industry": "food_beverage",
        "market_size": "local",
        "technology_requirements": [
            "Kitchen management system",
            "Reservation platform",
            "Inventory tracking",
        ],
        "regulatory_requirements": [
            "Food safety certification",
            "Liquor license",
            "Health department permits",
        ],
    },
    "ecommerce": {
        "business_name": "EcoStyle Fashion",
        "business_type": "ecommerce",
        "location": "London, UK",
        "description": "Sustainable fashion e-commerce platform selling eco-friendly clothing and accessories",
        "target_market": "Environmentally conscious consumers aged 18-40 who prioritize sustainable fashion",
        "competitors": ["Patagonia", "Reformation", "Everlane"],
        "growth_goals": [
            "Reach 50,000 customers",
            "Expand to 10 European countries",
            "Launch private label",
        ],
        "initial_investment": 150000.0,
        "team_size": 12,
        "unique_value_proposition": "Curated sustainable fashion with transparent supply chain and carbon-neutral shipping",
        "business_model": "b2c",
        "industry": "retail",
        "market_size": "international",
        "technology_requirements": [
            "E-commerce platform",
            "Payment processing",
            "Inventory management",
            "Shipping integration",
        ],
        "regulatory_requirements": [
            "GDPR compliance",
            "Consumer protection laws",
            "Import/export regulations",
        ],
    },
}


async def analyze_business(business_data):
    """Analyze a business using the multi-agent system"""
    print(f"\n🚀 Analyzing: {business_data['business_name']}")
    print(f"📍 Location: {business_data['location']}")
    print(f"🏢 Type: {business_data['business_type']}")
    print(f"💰 Investment: ${business_data.get('initial_investment', 'N/A'):,}")

    async with httpx.AsyncClient(timeout=120.0) as client:
        try:
            start_time = datetime.now()

            response = await client.post(
                f"{CORE_AGENT_URL}/process-business",
                json=business_data,
                headers={"Content-Type": "application/json"},
            )

            end_time = datetime.now()
            processing_time = (end_time - start_time).total_seconds()

            if response.status_code == 200:
                result = response.json()
                print(f"✅ Analysis completed in {processing_time:.2f} seconds")

                # Display key insights
                display_key_insights(result)
                return True
            else:
                print(f"❌ Analysis failed (Status: {response.status_code})")
                print(f"Response: {response.text}")
                return False

        except Exception as e:
            print(f"❌ Error during analysis: {e}")
            return False


def display_key_insights(result):
    """Display key insights from the analysis"""
    print("\n📊 Key Insights:")
    print("-" * 40)

    # Strategic insights
    strategic = result.get("strategic_plan", {})
    if strategic:
        positioning = strategic.get("competitive_positioning", {})
        print(
            f"🎯 Market Position: {positioning.get('unique_value_proposition', 'N/A')}"
        )

        growth = strategic.get("growth_strategy", {})
        short_term_goals = growth.get("short_term_goals", [])
        print(f"📈 Growth Goals: {len(short_term_goals)} short-term objectives")

    # Financial insights
    financial = result.get("financial_analysis", {})
    if financial:
        projections = financial.get("financial_projections", {})
        revenue = projections.get("revenue_forecast", {})
        print(f"💰 Revenue Forecast (Year 1): {revenue.get('year_1', 'N/A')}")

        funding = financial.get("funding_requirements", {})
        investment = funding.get("initial_investment", {}).get("total", "N/A")
        print(f"💵 Initial Investment: {investment}")

    # Success probability
    analytics = result.get("analytics_summary", {})
    if analytics:
        success = analytics.get("success_probability", {})
        success_rate = success.get("overall_success_rate", "N/A")
        print(f"🎯 Success Probability: {success_rate}")

    # Top recommendations
    recommendations = result.get("overall_recommendations", [])
    if recommendations:
        print(f"\n💡 Top 3 Recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"   {i}. {rec}")

    print("-" * 40)


async def demo_all_business_types():
    """Demonstrate analysis for all business types"""
    print("🎭 Multi-Agent Business Analysis System - Dynamic Input Demo")
    print("=" * 60)
    print("This demo shows how the system adapts its analysis based on business type.")
    print("Each business type will receive customized analysis from our AI agents.\n")

    # Wait for system to be ready
    print("⏳ Waiting for system to be ready...")
    await asyncio.sleep(3)

    success_count = 0
    total_count = len(BUSINESS_EXAMPLES)

    for business_type, business_data in BUSINESS_EXAMPLES.items():
        success = await analyze_business(business_data)
        if success:
            success_count += 1

        # Add delay between analyses
        if business_type != list(BUSINESS_EXAMPLES.keys())[-1]:
            print("\n⏳ Waiting 5 seconds before next analysis...")
            await asyncio.sleep(5)

    print(f"\n🎉 Demo completed!")
    print(f"✅ Successful analyses: {success_count}/{total_count}")
    print(f"📊 Success rate: {(success_count/total_count)*100:.1f}%")


async def demo_single_business_type(business_type):
    """Demonstrate analysis for a single business type"""
    if business_type not in BUSINESS_EXAMPLES:
        print(f"❌ Unknown business type: {business_type}")
        print(f"Available types: {list(BUSINESS_EXAMPLES.keys())}")
        return

    print(f"🎭 Single Business Type Demo: {business_type}")
    print("=" * 50)

    business_data = BUSINESS_EXAMPLES[business_type]
    await analyze_business(business_data)


async def main():
    """Main demo function"""
    import sys

    if len(sys.argv) > 1:
        business_type = sys.argv[1].lower()
        await demo_single_business_type(business_type)
    else:
        await demo_all_business_types()


if __name__ == "__main__":
    asyncio.run(main())
