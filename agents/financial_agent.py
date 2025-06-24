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

app = FastAPI(title="Financial Agent", version="1.0.0")

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


class FinancialResponse(BaseModel):
    agent_type: str
    financial_analysis: Dict[str, Any]
    timestamp: str
    request_id: str


class FinancialAgent:
    """Financial Agent for financial analysis and planning"""

    def __init__(self):
        self.agent_type = "financial"

    async def analyze_financial_aspects(
        self, business_data: Dict[str, Any], strategic_plan: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze financial aspects of the business"""

        business_name = business_data.get("business_name", "")
        location = business_data.get("location", "")
        growth_goals = business_data.get("growth_goals", [])

        # Create prompt for financial analysis
        prompt = f"""
        As a financial consultant specializing in small business finance, analyze the following business and provide financial recommendations:

        Business Name: {business_name}
        Location: {location}
        Growth Goals: {', '.join(growth_goals)}
        
        Strategic Plan Context: {strategic_plan.get('growth_strategy', {}).get('short_term_goals', [])}

        Please provide financial analysis including:
        1. Financial projections and forecasts
        2. Funding requirements and sources
        3. Cost structure analysis
        4. Pricing strategy recommendations
        5. Cash flow management
        6. Investment opportunities
        7. Financial risk assessment
        8. Break-even analysis

        Focus on practical financial strategies for a coffee shop business in Thailand.
        """

        try:
            # Call OpenAI for financial analysis
            response = await openai.ChatCompletion.acreate(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert financial consultant specializing in small business finance, particularly in the food and beverage industry in Thailand.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=1200,
                temperature=0.7,
            )

            financial_analysis_text = response.choices[0].message.content

            # Structure the financial analysis
            financial_analysis = {
                "business_name": business_name,
                "financial_projections": {
                    "revenue_forecast": {
                        "year_1": "2,500,000 THB",
                        "year_2": "3,750,000 THB",
                        "year_3": "5,000,000 THB",
                    },
                    "profit_margins": {
                        "coffee_products": "65-70%",
                        "food_items": "55-60%",
                        "merchandise": "40-50%",
                    },
                    "monthly_revenue_targets": {
                        "month_1_6": "150,000 THB",
                        "month_7_12": "250,000 THB",
                        "year_2": "312,500 THB",
                    },
                },
                "funding_requirements": {
                    "initial_investment": {
                        "equipment": "800,000 THB",
                        "renovation": "500,000 THB",
                        "inventory": "200,000 THB",
                        "marketing": "300,000 THB",
                        "working_capital": "200,000 THB",
                        "total": "2,000,000 THB",
                    },
                    "funding_sources": [
                        {
                            "source": "Personal savings",
                            "amount": "1,000,000 THB",
                            "percentage": "50%",
                        },
                        {
                            "source": "Bank loan",
                            "amount": "800,000 THB",
                            "percentage": "40%",
                        },
                        {
                            "source": "Investor/Partner",
                            "amount": "200,000 THB",
                            "percentage": "10%",
                        },
                    ],
                },
                "cost_structure": {
                    "fixed_costs": {
                        "rent": "50,000 THB/month",
                        "utilities": "15,000 THB/month",
                        "insurance": "5,000 THB/month",
                        "licenses": "2,000 THB/month",
                        "total_fixed": "72,000 THB/month",
                    },
                    "variable_costs": {
                        "coffee_beans": "25% of revenue",
                        "milk_and_syrups": "8% of revenue",
                        "packaging": "5% of revenue",
                        "labor": "30% of revenue",
                        "total_variable": "68% of revenue",
                    },
                },
                "pricing_strategy": {
                    "coffee_prices": {
                        "espresso": "35-45 THB",
                        "americano": "45-55 THB",
                        "latte": "55-65 THB",
                        "cappuccino": "55-65 THB",
                        "specialty_drinks": "65-85 THB",
                    },
                    "food_prices": {
                        "pastries": "45-65 THB",
                        "sandwiches": "85-120 THB",
                        "desserts": "65-95 THB",
                    },
                    "pricing_factors": [
                        "Competitor analysis",
                        "Cost-plus pricing",
                        "Value-based pricing",
                        "Premium positioning",
                    ],
                },
                "cash_flow_management": {
                    "daily_cash_flow": {
                        "inflow": "8,000-12,000 THB",
                        "outflow": "6,000-8,000 THB",
                        "net": "2,000-4,000 THB",
                    },
                    "cash_reserves": "Maintain 3-6 months of operating expenses",
                    "payment_terms": {
                        "suppliers": "Net 30 days",
                        "customers": "Immediate payment",
                        "utilities": "Monthly in advance",
                    },
                },
                "investment_opportunities": [
                    {
                        "opportunity": "Equipment upgrade",
                        "investment": "300,000 THB",
                        "roi": "15-20%",
                        "payback_period": "18-24 months",
                    },
                    {
                        "opportunity": "Digital ordering system",
                        "investment": "150,000 THB",
                        "roi": "25-30%",
                        "payback_period": "12-18 months",
                    },
                    {
                        "opportunity": "Marketing campaign",
                        "investment": "200,000 THB",
                        "roi": "20-25%",
                        "payback_period": "6-12 months",
                    },
                ],
                "financial_risks": {
                    "market_risks": [
                        "Economic downturn affecting discretionary spending",
                        "Changes in coffee prices",
                        "New competitors entering the market",
                    ],
                    "operational_risks": [
                        "Staff turnover and training costs",
                        "Equipment breakdowns",
                        "Supply chain disruptions",
                    ],
                    "mitigation_strategies": [
                        "Diversify revenue streams",
                        "Build emergency fund",
                        "Maintain good supplier relationships",
                        "Invest in staff training and retention",
                    ],
                },
                "break_even_analysis": {
                    "monthly_fixed_costs": "72,000 THB",
                    "average_contribution_margin": "32%",
                    "break_even_revenue": "225,000 THB/month",
                    "break_even_customers": "1,500 customers/month",
                    "break_even_timeframe": "8-12 months",
                },
                "financial_kpis": [
                    "Daily sales revenue",
                    "Customer average transaction value",
                    "Cost of goods sold (COGS)",
                    "Gross profit margin",
                    "Net profit margin",
                    "Cash flow from operations",
                    "Return on investment (ROI)",
                    "Customer acquisition cost",
                ],
                "recommendations": [
                    "Start with conservative financial projections and adjust based on actual performance",
                    "Maintain a cash reserve of at least 6 months of operating expenses",
                    "Implement cost control measures and regular financial monitoring",
                    "Consider multiple funding sources to reduce financial risk",
                    "Focus on high-margin products and efficient operations",
                    "Invest in technology to improve operational efficiency",
                    "Build strong relationships with suppliers for better payment terms",
                    "Regularly review and adjust pricing strategy based on market conditions",
                ],
                "ai_analysis": financial_analysis_text,
            }

            return financial_analysis

        except Exception as e:
            # Fallback to predefined financial analysis if OpenAI fails
            return {
                "business_name": business_name,
                "financial_projections": {
                    "revenue_forecast": {
                        "year_1": "2,500,000 THB",
                        "year_2": "3,750,000 THB",
                    }
                },
                "funding_requirements": {
                    "initial_investment": {"total": "2,000,000 THB"}
                },
                "pricing_strategy": {
                    "coffee_prices": {"latte": "55-65 THB", "americano": "45-55 THB"}
                },
                "recommendations": [
                    "Maintain cash reserves",
                    "Monitor costs closely",
                    "Focus on high-margin products",
                    "Build supplier relationships",
                ],
            }


# Initialize financial agent
financial_agent = FinancialAgent()


@app.post("/receive_message", response_model=FinancialResponse)
async def receive_message(message: MCPMessage):
    """Receive and process messages from Core Agent"""
    try:
        financial_analysis = await financial_agent.analyze_financial_aspects(
            message.business_data, message.strategic_plan
        )

        return FinancialResponse(
            agent_type=message.agent_type,
            financial_analysis=financial_analysis,
            timestamp=datetime.now().isoformat(),
            request_id=message.request_id,
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Financial analysis failed: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_type": "financial",
        "timestamp": datetime.now().isoformat(),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5003)
