#!/usr/bin/env python3
"""
Test script for Multi-Agent Business Analysis System
Tests the complete workflow with sample business data
"""

import asyncio
import httpx
import json
import time
from datetime import datetime

# Test configuration
CORE_AGENT_URL = "http://localhost:5099"
TEST_BUSINESS_DATA = {
    "business_name": "ร้านกาแฟสดใจดี",
    "location": "กรุงเทพมหานคร",
    "competitors": ["ร้านกาแฟ Amazon", "ร้านกาแฟ All Cafe"],
    "growth_goals": ["เพิ่มยอดขาย 50% ภายใน 1 ปี", "ขยายสาขาใหม่"],
}


async def test_health_endpoints():
    """Test health endpoints of all agents"""
    print("🔍 Testing health endpoints...")

    agents = [
        ("Core Agent", "http://localhost:5099/health"),
        ("Strategic Agent", "http://localhost:5001/health"),
        ("Creative Agent", "http://localhost:5002/health"),
        ("Financial Agent", "http://localhost:5003/health"),
        ("Sales Agent", "http://localhost:5004/health"),
        ("Manager Agent", "http://localhost:5005/health"),
        ("Analytics Agent", "http://localhost:5006/health"),
        ("SWOT Agent", "http://localhost:5007/health"),
        ("Business Model Canvas Agent", "http://localhost:5008/health"),
    ]

    async with httpx.AsyncClient(timeout=10.0) as client:
        for name, url in agents:
            try:
                response = await client.get(url)
                if response.status_code == 200:
                    print(f"✓ {name}: Healthy")
                else:
                    print(f"✗ {name}: Unhealthy (Status: {response.status_code})")
            except Exception as e:
                print(f"✗ {name}: Error - {e}")


async def test_business_analysis():
    """Test the complete business analysis workflow"""
    print("\n🚀 Testing business analysis workflow...")

    async with httpx.AsyncClient(
        timeout=120.0
    ) as client:  # Increased timeout for more agents
        try:
            # Send business analysis request
            print("📤 Sending business analysis request...")
            start_time = time.time()

            response = await client.post(
                f"{CORE_AGENT_URL}/process-business",
                json=TEST_BUSINESS_DATA,
                headers={"Content-Type": "application/json"},
            )

            end_time = time.time()
            processing_time = end_time - start_time

            if response.status_code == 200:
                print(
                    f"✓ Business analysis completed successfully in {processing_time:.2f} seconds"
                )

                # Parse and display results
                result = response.json()
                display_results(result)

                return True
            else:
                print(f"✗ Business analysis failed (Status: {response.status_code})")
                print(f"Response: {response.text}")
                return False

        except Exception as e:
            print(f"✗ Error during business analysis: {e}")
            return False


def display_results(result):
    """Display the analysis results in a formatted way"""
    print("\n📊 Business Analysis Results")
    print("=" * 50)

    print(f"Business: {result.get('business_name', 'N/A')}")
    print(f"Timestamp: {result.get('timestamp', 'N/A')}")

    # Strategic Plan Summary
    strategic = result.get("strategic_plan", {})
    print(f"\n🎯 Strategic Plan:")
    print(
        f"  • Market Position: {strategic.get('competitive_positioning', {}).get('unique_value_proposition', 'N/A')}"
    )
    print(
        f"  • Growth Strategy: {len(strategic.get('growth_strategy', {}).get('short_term_goals', []))} short-term goals"
    )
    print(
        f"  • Key Recommendations: {len(strategic.get('key_recommendations', []))} recommendations"
    )

    # SWOT Analysis Summary
    swot = result.get("swot_analysis", {})
    print(f"\n📋 SWOT Analysis:")
    strengths = swot.get("strengths", {}).get("internal_advantages", [])
    weaknesses = swot.get("weaknesses", {}).get("internal_limitations", [])
    opportunities = swot.get("opportunities", {}).get("market_trends", [])
    threats = swot.get("threats", {}).get("market_risks", [])
    print(f"  • Strengths: {len(strengths)} identified")
    print(f"  • Weaknesses: {len(weaknesses)} identified")
    print(f"  • Opportunities: {len(opportunities)} identified")
    print(f"  • Threats: {len(threats)} identified")

    # Business Model Canvas Summary
    bmc = result.get("business_model_canvas", {})
    print(f"\n🏗️  Business Model Canvas:")
    key_partners = bmc.get("key_partners", {}).get("suppliers", [])
    value_props = bmc.get("value_propositions", {}).get("secondary_values", [])
    customer_segments = bmc.get("customer_segments", {}).get("primary_segments", [])
    revenue_streams = bmc.get("revenue_streams", {}).get("primary_streams", [])
    print(f"  • Key Partners: {len(key_partners)} suppliers")
    print(f"  • Value Propositions: {len(value_props)} secondary values")
    print(f"  • Customer Segments: {len(customer_segments)} primary segments")
    print(f"  • Revenue Streams: {len(revenue_streams)} primary streams")

    # Creative Analysis Summary
    creative = result.get("creative_analysis", {})
    print(f"\n🎨 Creative Analysis:")
    print(
        f"  • Brand Personality: {creative.get('brand_identity', {}).get('brand_personality', 'N/A')}"
    )
    print(
        f"  • Marketing Campaigns: {len(creative.get('marketing_campaigns', []))} campaigns"
    )
    print(
        f"  • Creative Recommendations: {len(creative.get('recommendations', []))} recommendations"
    )

    # Financial Analysis Summary
    financial = result.get("financial_analysis", {})
    print(f"\n💰 Financial Analysis:")
    revenue_forecast = financial.get("financial_projections", {}).get(
        "revenue_forecast", {}
    )
    print(f"  • Revenue Forecast: {revenue_forecast.get('year_1', 'N/A')} (Year 1)")
    investment = (
        financial.get("funding_requirements", {})
        .get("initial_investment", {})
        .get("total", "N/A")
    )
    print(f"  • Initial Investment: {investment}")
    break_even = financial.get("break_even_analysis", {}).get(
        "break_even_revenue", "N/A"
    )
    print(f"  • Break-even Revenue: {break_even}")

    # Sales Strategy Summary
    sales = result.get("sales_strategy", {})
    print(f"\n📈 Sales Strategy:")
    segments = sales.get("target_customer_segments", {})
    print(f"  • Target Segments: {len(segments)} customer segments")
    channels = sales.get("sales_channels", {})
    print(f"  • Sales Channels: {len(channels)} channel types")
    targets = sales.get("sales_metrics", {}).get("targets", {})
    print(f"  • Monthly Revenue Target: {targets.get('monthly_revenue', 'N/A')}")

    # Analytics Summary
    analytics = result.get("analytics_summary", {})
    print(f"\n📊 Analytics Summary:")
    success_rate = analytics.get("success_probability", {}).get(
        "overall_success_rate", "N/A"
    )
    print(f"  • Success Probability: {success_rate}")
    insights = analytics.get("key_insights", [])
    print(f"  • Key Insights: {len(insights)} insights")

    # Overall Recommendations
    recommendations = result.get("overall_recommendations", [])
    print(f"\n💡 Overall Recommendations ({len(recommendations)} total):")
    for i, rec in enumerate(recommendations[:5], 1):  # Show first 5
        print(f"  {i}. {rec}")
    if len(recommendations) > 5:
        print(f"  ... and {len(recommendations) - 5} more recommendations")


async def test_individual_agents():
    """Test individual agent endpoints"""
    print("\n🧪 Testing individual agent endpoints...")

    agents = [
        ("Strategic", "http://localhost:5001/receive_message"),
        ("Creative", "http://localhost:5002/receive_message"),
        ("Financial", "http://localhost:5003/receive_message"),
        ("Sales", "http://localhost:5004/receive_message"),
        ("SWOT", "http://localhost:5007/receive_message"),
        ("Business Model Canvas", "http://localhost:5008/receive_message"),
        ("Analytics", "http://localhost:5006/receive_message"),
    ]

    async with httpx.AsyncClient(timeout=30.0) as client:
        for name, url in agents:
            try:
                test_message = {
                    "agent_type": name.lower().replace(" ", "_"),
                    "business_data": TEST_BUSINESS_DATA,
                    "timestamp": datetime.now().isoformat(),
                    "request_id": f"test_{name.lower().replace(' ', '_')}_{int(time.time())}",
                }

                response = await client.post(url, json=test_message)
                if response.status_code == 200:
                    print(f"✓ {name} Agent: Working")
                else:
                    print(f"✗ {name} Agent: Failed (Status: {response.status_code})")

            except Exception as e:
                print(f"✗ {name} Agent: Error - {e}")


async def main():
    """Main test function"""
    print("🧪 Multi-Agent Business Analysis System Test")
    print("=" * 50)

    # Wait for system to be ready
    print("⏳ Waiting for system to be ready...")
    await asyncio.sleep(5)

    # Test health endpoints
    await test_health_endpoints()

    # Test individual agents
    await test_individual_agents()

    # Test complete workflow
    success = await test_business_analysis()

    if success:
        print("\n🎉 All tests completed successfully!")
        print("✅ The Multi-Agent Business Analysis System is working correctly.")
    else:
        print("\n❌ Some tests failed.")
        print("🔧 Please check the system configuration and try again.")


if __name__ == "__main__":
    asyncio.run(main())
