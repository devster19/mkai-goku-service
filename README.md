# Multi-Agent Business Analysis System API

A FastAPI-based backend system for multi-agent business analysis with MCP (Model Context Protocol) task management.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MongoDB
- Virtual environment

### Installation
```bash
# Clone the repository
git clone <repository-url>
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
python3 -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

---

## 🏢 Business Management

### Create Business
**POST** `/business/create`

Creates a new business with minimal required fields.

#### Request Body
```json
{
  "business_name": "string",           // REQUIRED: Name of the business
  "description": "string",             // REQUIRED: Brief description
  "business_type": "string",           // OPTIONAL: Type of business (default: "retail_store")
  "location": "string",                // OPTIONAL: Business location (default: "Bangkok")
  "target_market": "string",           // OPTIONAL: Target market (default: "general")
  "competitors": ["string"],           // OPTIONAL: List of competitors (default: [])
  "growth_goals": ["string"]           // OPTIONAL: Growth objectives (default: [])
}
```

#### Example Request
```bash
curl -X POST "http://localhost:8000/api/v1/business/create" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Looknam Premium Lotion Tissue",
    "description": "Premium tissue products with lotion",
    "business_type": "retail_store",
    "location": "Bangkok, Thailand",
    "target_market": "Health-conscious consumers",
    "competitors": ["Kleenex", "Puffs"],
    "growth_goals": ["Expand to online sales", "Enter new markets"]
  }'
```

#### Response
```json
{
  "business_id": "685e0265ee376ed320ab6609",
  "business_name": "Looknam Premium Lotion Tissue",
  "business_type": "retail_store",
  "location": "Bangkok, Thailand",
  "description": "Premium tissue products with lotion",
  "target_market": "Health-conscious consumers",
  "competitors": ["Kleenex", "Puffs"],
  "growth_goals": ["Expand to online sales", "Enter new markets"],
  "initial_investment": null,
  "team_size": null,
  "unique_value_proposition": null,
  "business_model": null,
  "industry": null,
  "market_size": null,
  "technology_requirements": null,
  "regulatory_requirements": null,
  "created_at": "2025-06-27T02:42:38.849452",
  "updated_at": "2025-06-27T02:42:38.849457"
}
```

### Get Business by ID
**GET** `/business/{business_id}`

Retrieves business information by ID.

#### Example Request
```bash
curl -X GET "http://localhost:8000/api/v1/business/685e0265ee376ed320ab6609"
```

#### Response
```json
{
  "business_id": "685e0265ee376ed320ab6609",
  "business_name": "Looknam Premium Lotion Tissue",
  "business_type": "retail_store",
  "location": "Bangkok, Thailand",
  "description": "Premium tissue products with lotion",
  "target_market": "Health-conscious consumers",
  "competitors": ["Kleenex", "Puffs"],
  "growth_goals": ["Expand to online sales", "Enter new markets"],
  "created_at": "2025-06-27T02:42:38.849452",
  "updated_at": "2025-06-27T02:42:38.849457"
}
```

---

## 🤖 Agent Management

### Get Agent Types
**GET** `/agents/types`

Retrieves all available agent types.

#### Query Parameters
- `category` (optional): Filter by category (e.g., "analysis", "creative", "financial")
- `active_only` (optional): Show only active types (default: true)

#### Example Request
```bash
curl -X GET "http://localhost:8000/api/v1/agents/types"
```

#### Response
```json
{
  "agent_types": [
    {
      "type_id": "analytics_agent",
      "name": "Analytics Agent",
      "description": "Performs data analysis and insights",
      "category": "analysis",
      "capabilities": ["data_analysis", "insights", "reporting"],
      "is_active": true,
      "version": "1.0.0"
    },
    {
      "type_id": "financial_agent",
      "name": "Financial Agent",
      "description": "Handles financial analysis and planning",
      "category": "financial",
      "capabilities": ["financial_analysis", "budgeting", "forecasting"],
      "is_active": true,
      "version": "1.0.0"
    }
  ],
  "total_count": 30,
  "category_filter": null
}
```

### Register Agent
**POST** `/agents/register`

Registers a new agent with the system.

#### Request Body
```json
{
  "agent_name": "string",              // REQUIRED: Name of the agent
  "agent_type": "string",              // REQUIRED: Type from available agent types
  "endpoint_url": "string",            // REQUIRED: URL where agent can be reached
  "api_key": "string",                 // OPTIONAL: API key for authentication
  "description": "string",             // OPTIONAL: Agent description
  "capabilities": ["string"],          // OPTIONAL: List of capabilities
  "callback_url": "string",            // OPTIONAL: URL for receiving results
  "status": "string",                  // OPTIONAL: Status (default: "active")
  "version": "string",                 // OPTIONAL: Version (default: "1.0.0")
  "contact_info": {},                  // OPTIONAL: Contact information
  "configuration": {},                 // OPTIONAL: Additional configuration
  "mcp_support": false                 // OPTIONAL: MCP protocol support (default: false)
}
```

#### Example Request
```bash
curl -X POST "http://localhost:8000/api/v1/agents/register" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "Test Analytics Agent",
    "agent_type": "analytics_agent",
    "endpoint_url": "http://localhost:3000/analytics",
    "api_key": "secret-api-key-123",
    "description": "Test analytics agent for business analysis",
    "capabilities": ["data_analysis", "insights"],
    "status": "active",
    "mcp_support": true
  }'
```

#### Response
```json
{
  "agent_id": "685e04a8e8205955866520f0",
  "agent_name": "Test Analytics Agent",
  "agent_type": "analytics_agent",
  "description": "Test analytics agent for business analysis",
  "capabilities": ["data_analysis", "insights"],
  "endpoint_url": "http://localhost:3000/analytics",
  "callback_url": null,
  "status": "active",
  "version": "1.0.0",
  "contact_info": null,
  "configuration": null,
  "mcp_support": true,
  "created_at": "2025-06-27T02:45:00.000000",
  "updated_at": "2025-06-27T02:45:00.000000"
}
```

### Update Agent
**PUT** `/agents/{agent_id}`

Updates an existing agent's information.

#### Request Body
```json
{
  "agent_name": "string",              // OPTIONAL: New agent name
  "description": "string",             // OPTIONAL: New description
  "capabilities": ["string"],          // OPTIONAL: Updated capabilities
  "endpoint_url": "string",            // OPTIONAL: New endpoint URL
  "callback_url": "string",            // OPTIONAL: New callback URL
  "api_key": "string",                 // OPTIONAL: New API key
  "status": "string",                  // OPTIONAL: New status
  "version": "string",                 // OPTIONAL: New version
  "contact_info": {},                  // OPTIONAL: Updated contact info
  "configuration": {},                 // OPTIONAL: Updated configuration
  "mcp_support": false                 // OPTIONAL: MCP support status
}
```

#### Example Request
```bash
curl -X PUT "http://localhost:8000/api/v1/agents/685e04a8e8205955866520f0" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated analytics agent description",
    "status": "active",
    "capabilities": ["data_analysis", "insights", "reporting"]
  }'
```

---

## 📋 MCP Task Management

### Create MCP Task
**POST** `/agents/mcp/task`

Creates a new MCP task that will be automatically assigned to an available agent.

#### Request Body
```json
{
  "query": "Analyze market trends for premium tissue products in Thailand for 2024–2025.",
  "type": "market_analysis",
  "params": {
    "market_segment": "premium_tissue",
    "geographic_region": "Thailand",
    "time_period": "2024-2025"
  },
  "business_id": "685e0265ee376ed320ab6609",
  "llm_params": {
    "model": "gpt-4-turbo",
    "temperature": 0.3,
    "max_tokens": 1200
  },
  "output_preferences": {
    "format": "markdown",
    "audience": "executive_summary"
  },
  "tools": {
    "enable_web_search": true,
    "use_internal_market_data": true
  }
}
```

#### Example Request
```bash
curl -X POST "http://localhost:8000/api/v1/agents/mcp/task" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze market trends for premium tissue products in Thailand for 2024–2025.",
    "type": "market_analysis",
    "params": {
      "market_segment": "premium_tissue",
      "geographic_region": "Thailand",
      "time_period": "2024-2025"
    },
    "business_id": "685e0265ee376ed320ab6609",
    "llm_params": {
      "model": "gpt-4-turbo",
      "temperature": 0.3,
      "max_tokens": 1200
    },
    "output_preferences": {
      "format": "markdown",
      "audience": "executive_summary"
    },
    "tools": {
      "enable_web_search": true,
      "use_internal_market_data": true
    }
  }'
```

#### Response
```json
{
  "task_id": "685e051ee8205955866520f1",
  "agent_id": "685e04a8e8205955866520f0",
  "business_id": "685e0265ee376ed320ab6609",
  "type": "market_analysis",
  "params": {
    "market_segment": "premium_tissue",
    "geographic_region": "Thailand",
    "time_period": "2024-2025"
  },
  "status": "pending",
  "result": null,
  "output": null,
  "context": null,
  "context_update": null,
  "callback_url": "http://localhost:8000/api/v1/agents/mcp/callback?task_id=Njg1ZTA1MWVlODIwNTk1NTg2NjUyMGYx&token=2d5ab9441fd29d9aee12a19c4b53260acdd1c37665afef037a064edc677abd4c&expires_at=1750995758&signature=NDcwODdkOTZhNDU5MzlmNmVkYmU0NmFhNzU1OTJhMGJmNjBjODg3NmE4NGU5ZD",
  "created_at": "2025-06-27T02:42:38.849452",
  "updated_at": "2025-06-27T02:42:38.849457"
}
```

### Get MCP Task
**GET** `/agents/mcp/task/{task_id}`

Retrieves a specific MCP task by ID.

#### Example Request
```bash
curl -X GET "http://localhost:8000/api/v1/agents/mcp/task/685e051ee8205955866520f1"
```

#### Response
```json
{
  "task_id": "685e051ee8205955866520f1",
  "agent_id": "685e04a8e8205955866520f0",
  "business_id": "685e0265ee376ed320ab6609",
  "type": "market_analysis",
  "params": {
    "market_segment": "premium_tissue",
    "geographic_region": "Thailand",
    "time_period": "2024-2025"
  },
  "status": "completed",
  "result": {
    "analysis_result": "Market analysis completed",
    "insights": ["Growing demand", "Premium positioning opportunity"]
  },
  "output": {
    "text": "Market analysis completed successfully",
    "data": {
      "market_size": "1.2B THB",
      "growth_rate": "8.5%",
      "key_insights": ["Premium segment growing", "Online sales opportunity"]
    }
  },
  "callback_url": "http://localhost:8000/api/v1/agents/mcp/callback?task_id=Njg1ZTA1MWVlODIwNTk1NTg2NjUyMGYx&token=2d5ab9441fd29d9aee12a19c4b53260acdd1c37665afef037a064edc677abd4c&expires_at=1750995758&signature=NDcwODdkOTZhNDU5MzlmNmVkYmU0NmFhNzU1OTJhMGJmNjBjODg3NmE4NGU5ZD",
  "created_at": "2025-06-27T02:42:38.849452",
  "updated_at": "2025-06-27T02:45:00.000000"
}
```

### Update Task via Callback

When a task is created, a secure callback URL is generated. Agents can use this URL to update task results.

#### Callback URL Format
```
http://localhost:8000/api/v1/agents/mcp/callback?task_id={encoded_task_id}&token={token}&expires_at={expires_at}&signature={signature}
```

#### **Simplified Request Body Format (RECOMMENDED)**

The callback endpoint now uses a clean, simplified format:

```json
{
  "output": {
    "text": "Task completion message",
    "data": { /* structured data */ },
    "images": [ /* image objects */ ],
    "links": [ /* link objects */ ],
    "files": [ /* file objects */ ],
    "html": "<html content>",
    "markdown": "# markdown content"
  },
  "context_update": {
    "memory": "Context memory update",
    "tags": ["tag1", "tag2"],
    "metadata": { /* metadata */ }
  },
  "execution_time": 2.5,
  "timestamp": "2025-06-27T05:45:00.000Z"
}
```

#### **Example Simplified Format Request**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/mcp/callback?task_id=Njg1ZTA1MWVlODIwNTk1NTg2NjUyMGYx&token=2d5ab9441fd29d9aee12a19c4b53260acdd1c37665afef037a064edc677abd4c&expires_at=1750995758&signature=NDcwODdkOTZhNDU5MzlmNmVkYmU0NmFhNzU1OTJhMGJmNjBjODg3NmE4NGU5ZD" \
  -H "Content-Type: application/json" \
  -d '{
    "output": {
      "text": "Market analysis completed successfully",
      "data": {
        "market_size": "1.2B THB",
        "growth_rate": "8.5%",
        "key_insights": ["Premium segment growing", "Online sales opportunity"]
      }
    },
    "context_update": {
      "memory": "Market analysis shows strong growth potential in premium segment",
      "tags": ["market_analysis", "premium_segment", "growth_opportunity"]
    },
    "execution_time": 2.5,
    "timestamp": "2025-06-27T02:45:00.000Z"
  }'
```

#### **Response Format**
The callback now returns the actual MCP result data instead of just task information:

```json
{
  "result_id": "685e20ba8e7ecf3da212d414",
  "task_id": "685e145d21891719b70f8f34",
  "agent_id": "685dde41b1efd54f0662ab32",
  "business_id": "685e0265ee376ed320ab6609",
  "status": "completed",
  "output": {
    "text": "Market analysis completed successfully",
    "images": [],
    "links": [],
    "files": [],
    "data": {
      "market_size": "1.2B THB",
      "growth_rate": "8.5%",
      "key_insights": ["Premium segment growing", "Online sales opportunity"]
    },
    "html": null,
    "markdown": null
  },
  "context_update": {
    "memory": "Market analysis shows strong growth potential in premium segment",
    "tags": ["market_analysis", "premium_segment", "growth_opportunity"],
    "metadata": null
  },
  "execution_time": 2.5,
  "error_message": null,
  "timestamp": "2025-06-27T04:40:26.851298",
  "created_at": "2025-06-27T04:40:26.851302"
}
```

#### **Minimal Example**
```bash
curl -X POST "http://localhost:8000/api/v1/agents/mcp/callback?task_id=Njg1ZTA1MWVlODIwNTk1NTg2NjUyMGYx&token=2d5ab9441fd29d9aee12a19c4b53260acdd1c37665afef037a064edc677abd4c&expires_at=1750995758&signature=NDcwODdkOTZhNDU5MzlmNmVkYmU0NmFhNzU1OTJhMGJmNjBjODg3NmE4NGU5ZD" \
  -H "Content-Type: application/json" \
  -d '{
    "output": {
      "text": "Task completed successfully"
    }
  }'
```

---

## 🎨 **Rich Content Callback Examples**

### **Example 1: Financial Analysis with Charts and Reports**

```bash
curl -X POST "http://localhost:8000/api/v1/agents/mcp/callback?task_id=Njg1ZGY4YmVjZTIxNDg1MTBhOTRkMTJi&token=3f2905648a82c8bdb6af14041a6bb74a8360e318d4df999c5f2039afef21a720&expires_at=1750992590&signature=ZDYxZjNhZWU0NGViNjY2YWNiYTMxYzJiMWRiNTZmNDE3YWViMjIwY2UwYThkNmE0YjM4ZmRmMTJiMDY5Y2EyYw" \
  -H "Content-Type: application/json" \
  -d '{
    "output": {
      "text": "Q4 2024 Financial Analysis completed with comprehensive insights and recommendations",
      "data": {
        "quarter": "Q4 2024",
        "revenue": "2.5M THB",
        "growth_rate": "18.5%",
        "profit_margin": "12.3%",
        "cash_flow": "positive",
        "key_metrics": {
          "revenue_growth": "18.5%",
          "profit_margin": "12.3%",
          "operating_expenses": "1.8M THB",
          "net_profit": "307K THB"
        },
        "forecast": {
          "next_quarter": "2.8M THB",
          "confidence_level": "85%",
          "assumptions": ["market growth", "new product launch", "expanded distribution"]
        }
      },
      "images": [
        {
          "url": "https://example.com/charts/revenue_trend_q4_2024.png",
          "caption": "Revenue Trend Q4 2024 - Strong growth in premium segment",
          "alt_text": "Line chart showing revenue growth from 2.1M to 2.5M THB",
          "type": "chart"
        },
        {
          "url": "https://example.com/charts/profit_margin_analysis.png",
          "caption": "Profit Margin Analysis - Improved efficiency",
          "alt_text": "Bar chart comparing profit margins across quarters",
          "type": "chart"
        },
        {
          "url": "https://example.com/charts/cash_flow_statement.png",
          "caption": "Cash Flow Statement - Positive operating cash flow",
          "alt_text": "Waterfall chart showing cash flow components",
          "type": "chart"
        }
      ],
      "links": [
        {
          "title": "Detailed Financial Report PDF",
          "url": "https://example.com/reports/financial_analysis_q4_2024.pdf",
          "description": "Comprehensive 25-page financial analysis report"
        },
        {
          "title": "Interactive Dashboard",
          "url": "https://example.com/dashboard/financial_q4_2024",
          "description": "Real-time interactive financial dashboard"
        },
        {
          "title": "Industry Benchmark Report",
          "url": "https://example.com/benchmarks/consumer_goods_2024.pdf",
          "description": "Industry comparison and benchmarking data"
        }
      ],
      "files": [
        {
          "filename": "financial_analysis_q4_2024.pdf",
          "url": "https://example.com/files/financial_analysis_q4_2024.pdf",
          "size": 2048576,
          "mime_type": "application/pdf"
        },
        {
          "filename": "financial_data_raw.xlsx",
          "url": "https://example.com/files/financial_data_raw.xlsx",
          "size": 512000,
          "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        },
        {
          "filename": "forecast_model.py",
          "url": "https://example.com/files/forecast_model.py",
          "size": 25600,
          "mime_type": "text/x-python"
        }
      ],
      "html": "<div class=\"financial-summary\"><h2>Q4 2024 Financial Summary</h2><p>Strong performance with <strong>18.5% revenue growth</strong> and improved profitability...</p></div>",
      "markdown": "# Q4 2024 Financial Analysis\n\n## Executive Summary\nStrong performance with **18.5% revenue growth** and improved profitability...\n\n## Key Findings\n- Revenue: 2.5M THB (+18.5%)\n- Profit Margin: 12.3% (+2.1%)\n- Cash Flow: Positive\n\n## Recommendations\n1. Continue premium segment focus\n2. Invest in digital transformation\n3. Expand to new markets"
    },
    "context_update": {
      "memory": "Q4 2024 showed strongest performance in company history with 18.5% growth. Premium segment now represents 45% of revenue. Cash flow positive for 6 consecutive quarters.",
      "tags": ["financial_analysis", "q4_2024", "strong_performance", "premium_segment"],
      "metadata": {
        "analysis_confidence": 0.95,
        "data_sources": ["internal_financial_system", "market_data", "competitor_analysis"],
        "next_review_date": "2025-03-31",
        "stakeholders": ["executive_team", "board_of_directors", "investors"]
      }
    },
    "execution_time": 45.2,
    "timestamp": "2025-06-27T02:45:00.000Z"
  }'
```

### **Example 2: Market Research with Visual Content**

```bash
curl -X POST "http://localhost:8000/api/v1/agents/mcp/callback?task_id=Njg1ZGY4YmVjZTIxNDg1MTBhOTRkMTJi&token=3f2905648a82c8bdb6af14041a6bb74a8360e318d4df999c5f2039afef21a720&expires_at=1750992590&signature=ZDYxZjNhZWU0NGViNjY2YWNiYTMxYzJiMWRiNTZmNDE3YWViMjIwY2UwYThkNmE0YjM4ZmRmMTJiMDY5Y2EyYw" \
  -H "Content-Type: application/json" \
  -d '{
    "output": {
      "text": "Comprehensive market research completed for premium tissue products in Southeast Asia",
      "data": {
        "market_size": "1.2B THB",
        "growth_rate": "8.5%",
        "target_markets": ["Thailand", "Singapore", "Malaysia"],
        "key_findings": {
          "premium_segment_growth": "12%",
          "online_sales_opportunity": "35%",
          "competitor_analysis": {
            "kleenex_market_share": "40%",
            "puffs_market_share": "25%",
            "local_brands": "35%"
          }
        },
        "swot_analysis": {
          "strengths": ["premium_quality", "local_manufacturing", "strong_distribution"],
          "weaknesses": ["brand_recognition", "limited_online_presence"],
          "opportunities": ["e-commerce_growth", "health_conscious_consumers"],
          "threats": ["intense_competition", "raw_material_costs"]
        }
      },
      "images": [
        {
          "url": "https://example.com/market_research/market_size_chart.png",
          "caption": "Market Size Growth Trend 2020-2024",
          "alt_text": "Bar chart showing market size growth from 800M to 1.2B THB",
          "type": "chart"
        },
        {
          "url": "https://example.com/market_research/competitor_analysis.png",
          "caption": "Competitor Market Share Analysis",
          "alt_text": "Pie chart showing market share distribution among competitors",
          "type": "chart"
        },
        {
          "url": "https://example.com/market_research/consumer_survey_results.png",
          "caption": "Consumer Survey Results - Brand Preferences",
          "alt_text": "Bar chart showing consumer brand preference survey results",
          "type": "chart"
        },
        {
          "url": "https://example.com/market_research/geographic_distribution.png",
          "caption": "Geographic Distribution of Premium Tissue Market",
          "alt_text": "Map showing premium tissue market distribution across Southeast Asia",
          "type": "map"
        }
      ],
      "links": [
        {
          "title": "Full Market Research Report",
          "url": "https://example.com/reports/market_research_premium_tissue_2024.pdf",
          "description": "Comprehensive 50-page market research report"
        },
        {
          "title": "Consumer Survey Data",
          "url": "https://example.com/data/consumer_survey_raw_data.xlsx",
          "description": "Raw consumer survey data and analysis"
        },
        {
          "title": "Competitor Profiles",
          "url": "https://example.com/competitors/competitor_profiles_2024.pdf",
          "description": "Detailed competitor analysis and profiles"
        }
      ],
      "files": [
        {
          "filename": "market_research_report_2024.pdf",
          "url": "https://example.com/files/market_research_report_2024.pdf",
          "size": 5120000,
          "mime_type": "application/pdf"
        },
        {
          "filename": "consumer_survey_data.xlsx",
          "url": "https://example.com/files/consumer_survey_data.xlsx",
          "size": 1024000,
          "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        },
        {
          "filename": "market_analysis_presentation.pptx",
          "url": "https://example.com/files/market_analysis_presentation.pptx",
          "size": 1536000,
          "mime_type": "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        }
      ],
      "html": "<div class=\"market-summary\"><h2>Market Research Summary</h2><p>Premium tissue market in Southeast Asia shows <strong>strong growth potential</strong> with 1.2B THB market size...</p></div>",
      "markdown": "# Market Research: Premium Tissue Products\n\n## Market Overview\n- **Market Size**: 1.2B THB\n- **Growth Rate**: 8.5%\n- **Target Markets**: Thailand, Singapore, Malaysia\n\n## Key Insights\n1. Premium segment growing at 12%\n2. Online sales opportunity: 35%\n3. Strong competition from established brands\n\n## Recommendations\n1. Focus on premium positioning\n2. Develop e-commerce strategy\n3. Build brand awareness"
    },
    "context_update": {
      "memory": "Premium tissue market in Southeast Asia is 1.2B THB with 8.5% growth. Online sales represent 35% opportunity. Strong competition from Kleenex (40%) and Puffs (25%). Local manufacturing and distribution are key advantages.",
      "tags": ["market_research", "premium_tissue", "southeast_asia", "competitive_analysis"],
      "metadata": {
        "research_methodology": ["surveys", "interviews", "data_analysis", "competitor_research"],
        "confidence_level": 0.92,
        "data_sources": ["industry_reports", "consumer_surveys", "competitor_analysis"],
        "next_update": "2025-03-15"
      }
    },
    "execution_time": 120.5,
    "timestamp": "2025-06-27T03:15:30.000Z"
  }'
```

### **Example 3: Data Analysis with Technical Output**

```bash
curl -X POST "http://localhost:8000/api/v1/agents/mcp/callback?task_id=Njg1ZGY4YmVjZTIxNDg1MTBhOTRkMTJi&token=3f2905648a82c8bdb6af14041a6bb74a8360e318d4df999c5f2039afef21a720&expires_at=1750992590&signature=ZDYxZjNhZWU0NGViNjY2YWNiYTMxYzJiMWRiNTZmNDE3YWViMjIwY2UwYThkNmE0YjM4ZmRmMTJiMDY5Y2EyYw" \
  -H "Content-Type: application/json" \
  -d '{
    "output": {
      "text": "Customer segmentation analysis completed with 5 distinct customer personas identified",
      "data": {
        "analysis_type": "customer_segmentation",
        "segments_identified": 5,
        "clustering_algorithm": "k_means",
        "segments": [
          {
            "segment_id": "premium_loyalists",
            "size": "25%",
            "characteristics": ["high_value", "loyal", "premium_products"],
            "avg_order_value": "2500 THB",
            "purchase_frequency": "monthly"
          },
          {
            "segment_id": "value_seekers",
            "size": "30%",
            "characteristics": ["price_sensitive", "bulk_purchases", "promotions"],
            "avg_order_value": "800 THB",
            "purchase_frequency": "weekly"
          },
          {
            "segment_id": "occasional_buyers",
            "size": "20%",
            "characteristics": ["infrequent", "basic_products", "convenience"],
            "avg_order_value": "500 THB",
            "purchase_frequency": "quarterly"
          },
          {
            "segment_id": "online_shoppers",
            "size": "15%",
            "characteristics": ["digital_native", "convenience", "reviews"],
            "avg_order_value": "1200 THB",
            "purchase_frequency": "bi_weekly"
          },
          {
            "segment_id": "business_customers",
            "size": "10%",
            "characteristics": ["bulk_orders", "contracts", "service_focused"],
            "avg_order_value": "5000 THB",
            "purchase_frequency": "monthly"
          }
        ],
        "model_performance": {
          "silhouette_score": 0.78,
          "inertia": 245.6,
          "convergence_iterations": 15
        }
      },
      "images": [
        {
          "url": "https://example.com/analytics/customer_segments_chart.png",
          "caption": "Customer Segmentation Results - 5 Distinct Segments",
          "alt_text": "Scatter plot showing 5 customer segments with different characteristics",
          "type": "chart"
        },
        {
          "url": "https://example.com/analytics/segment_characteristics.png",
          "caption": "Segment Characteristics Comparison",
          "alt_text": "Radar chart comparing characteristics across customer segments",
          "type": "chart"
        },
        {
          "url": "https://example.com/analytics/purchase_patterns.png",
          "caption": "Purchase Patterns by Segment",
          "alt_text": "Heatmap showing purchase patterns and frequencies by segment",
          "type": "chart"
        }
      ],
      "links": [
        {
          "title": "Interactive Segmentation Dashboard",
          "url": "https://example.com/dashboard/customer_segmentation",
          "description": "Interactive dashboard for exploring customer segments"
        },
        {
          "title": "Segmentation Model Documentation",
          "url": "https://example.com/docs/segmentation_model_technical.pdf",
          "description": "Technical documentation of the segmentation model"
        }
      ],
      "files": [
        {
          "filename": "customer_segmentation_model.pkl",
          "url": "https://example.com/models/customer_segmentation_model.pkl",
          "size": 512000,
          "mime_type": "application/octet-stream"
        },
        {
          "filename": "segmentation_analysis_report.pdf",
          "url": "https://example.com/reports/segmentation_analysis_report.pdf",
          "size": 2048000,
          "mime_type": "application/pdf"
        },
        {
          "filename": "customer_data_processed.csv",
          "url": "https://example.com/data/customer_data_processed.csv",
          "size": 256000,
          "mime_type": "text/csv"
        }
      ],
      "html": "<div class=\"segmentation-summary\"><h2>Customer Segmentation Results</h2><p>Successfully identified <strong>5 distinct customer segments</strong> with clear characteristics and behaviors...</p></div>",
      "markdown": "# Customer Segmentation Analysis\n\n## Overview\nSuccessfully identified **5 distinct customer segments** using K-means clustering.\n\n## Segments\n1. **Premium Loyalists** (25%) - High value, loyal customers\n2. **Value Seekers** (30%) - Price sensitive, bulk purchases\n3. **Occasional Buyers** (20%) - Infrequent, basic products\n4. **Online Shoppers** (15%) - Digital native, convenience focused\n5. **Business Customers** (10%) - Bulk orders, service focused\n\n## Model Performance\n- Silhouette Score: 0.78 (Good)\n- Convergence: 15 iterations\n- Data Quality: High"
    },
    "context_update": {
      "memory": "Customer base successfully segmented into 5 distinct groups. Premium Loyalists (25%) and Value Seekers (30%) are largest segments. Online Shoppers segment shows highest growth potential. Model performance is good with 0.78 silhouette score.",
      "tags": ["customer_segmentation", "k_means", "analytics", "customer_insights"],
      "metadata": {
        "model_version": "1.0",
        "data_points": 15000,
        "features_used": ["purchase_frequency", "avg_order_value", "product_categories", "geographic_location"],
        "next_analysis": "2025-03-01"
      }
    },
    "execution_time": 180.3,
    "timestamp": "2025-06-27T04:30:15.000Z"
  }'
```

### **Example 4: Minimal Update (Simple Format)**

```bash
curl -X POST "http://localhost:8000/api/v1/agents/mcp/callback?task_id=Njg1ZGY4YmVjZTIxNDg1MTBhOTRkMTJi&token=3f2905648a82c8bdb6af14041a6bb74a8360e318d4df999c5f2039afef21a720&expires_at=1750992590&signature=ZDYxZjNhZWU0NGViNjY2YWNiYTMxYzJiMWRiNTZmNDE3YWViMjIwY2UwYThkNmE0YjM4ZmRmMTJiMDY5Y2EyYw" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Task completed successfully",
    "data": {
      "result": "success",
      "score": 95
    },
    "execution_time": 2.5,
    "timestamp": "2025-06-27T02:45:00.000Z"
  }'
```

---

## 🔄 **Complete MCP Protocol Examples**

### **Example 1: Financial Analysis Task (Full MCP Format)**

```bash
curl -X POST "http://localhost:8000/api/v1/agents/mcp/task" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Analyze quarterly financial performance and provide recommendations",
    "type": "financial_analysis",
    "params": {
      "quarter": "Q4 2024",
      "analysis_type": "comprehensive",
      "include_forecasting": true,
      "metrics": ["revenue", "profit_margin", "cash_flow", "growth_rate"],
      "comparison_period": "Q3 2024",
      "include_benchmarks": true
    },
    "context": {
      "memory": "Previous quarters showed 15% growth with strong cash flow",
      "retriever": [
        "financial_data_2024",
        "market_trends",
        "competitor_analysis",
        "industry_benchmarks"
      ]
    },
    "business_id": "685e0265ee376ed320ab6609"
  }'
```

**Expected Response:**
```json
{
  "task_id": "685df8bece2148510a94d12b",
  "agent_id": "685dde41b1efd54f0662ab32",
  "business_id": "685e0265ee376ed320ab6609",
  "type": "financial_analysis",
  "params": {
    "quarter": "Q4 2024",
    "analysis_type": "comprehensive",
    "include_forecasting": true,
    "metrics": ["revenue", "profit_margin", "cash_flow", "growth_rate"],
    "comparison_period": "Q3 2024",
    "include_benchmarks": true
  },
  "status": "pending",
  "result": null,
  "output": null,
  "context": {
    "memory": "Previous quarters showed 15% growth with strong cash flow",
    "retriever": [
      "financial_data_2024",
      "market_trends",
      "competitor_analysis",
      "industry_benchmarks"
    ]
  },
  "context_update": null,
  "callback_url": "http://localhost:8000/api/v1/agents/mcp/callback?task_id=Njg1ZGY4YmVjZTIxNDg1MTBhOTRkMTJi&token=3f2905648a82c8bdb6af14041a6bb74a8360e318d4df999c5f2039afef21a720&expires_at=1750992590&signature=ZDYxZjNhZWU0NGViNjY2YWNiYTMxYzJiMWRiNTZmNDE3YWViMjIwY2UwYThkNmE0YjM4ZmRmMTJiMDY5Y2EyYw",
  "created_at": "2025-06-27T01:49:50.418541",
  "updated_at": "2025-06-27T01:49:50.418541"
}
```

### **Example 2: Content Generation Task (MCP with Context)**

```bash
curl -X POST "http://localhost:8000/api/v1/agents/mcp/task" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Generate comprehensive business strategy document",
    "type": "content_generation",
    "params": {
      "content_type": "business_strategy",
      "target_audience": "executive_team",
      "format": "markdown",
      "sections": [
        "executive_summary",
        "market_analysis",
        "competitive_positioning",
        "strategic_initiatives",
        "financial_projections"
      ],
      "word_count": 5000,
      "include_charts": true
    },
    "context": {
      "memory": "Company is expanding into Southeast Asian markets with focus on premium products",
      "retriever": [
        "business_plan_2024",
        "market_research_data",
        "competitor_profiles",
        "financial_forecasts"
      ]
    },
    "business_id": "685e0265ee376ed320ab6609"
  }'
```

### **Example 3: Market Research Task (MCP with Advanced Parameters)**

```bash
curl -X POST "http://localhost:8000/api/v1/agents/mcp/task" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Conduct comprehensive market research for new product launch",
    "type": "market_research",
    "params": {
      "research_scope": "comprehensive",
      "target_markets": ["Thailand", "Singapore", "Malaysia"],
      "research_methods": [
        "competitive_analysis",
        "customer_surveys",
        "trend_analysis",
        "pricing_study"
      ],
      "product_category": "premium_consumer_goods",
      "timeline": "3_months",
      "budget_range": "50000-100000",
      "include_swot_analysis": true,
      "generate_recommendations": true
    },
    "context": {
      "memory": "Previous market entry in Indonesia was successful with 25% market share",
      "retriever": [
        "indonesia_market_data",
        "competitor_analysis_2024",
        "consumer_behavior_studies",
        "regulatory_requirements"
      ]
    },
    "business_id": "685e0265ee376ed320ab6609"
  }'
```

### **Example 4: Data Analysis Task (MCP with Technical Context)**

```bash
curl -X POST "http://localhost:8000/api/v1/agents/mcp/task" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Analyze customer behavior patterns and segment customer base",
    "type": "data_analysis",
    "params": {
      "analysis_type": "customer_segmentation",
      "data_sources": [
        "transaction_history",
        "website_analytics",
        "customer_surveys",
        "social_media_data"
      ],
      "time_period": "last_12_months",
      "segmentation_criteria": [
        "purchase_frequency",
        "average_order_value",
        "product_categories",
        "geographic_location"
      ],
      "clustering_algorithm": "k_means",
      "number_of_segments": 5,
      "include_visualizations": true,
      "generate_insights": true
    },
    "context": {
      "memory": "Previous segmentation identified 4 key customer personas with distinct buying patterns",
      "retriever": [
        "customer_data_warehouse",
        "previous_segmentation_results",
        "marketing_campaign_data",
        "product_performance_metrics"
      ]
    },
    "business_id": "685e0265ee376ed320ab6609"
  }'
```

### **Example 5: Strategic Planning Task (MCP with Business Context)**

```bash
curl -X POST "http://localhost:8000/api/v1/agents/mcp/task" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Develop 3-year strategic roadmap for business expansion",
    "type": "strategic_planning",
    "params": {
      "planning_horizon": "3_years",
      "focus_areas": [
        "market_expansion",
        "product_development",
        "operational_efficiency",
        "digital_transformation"
      ],
      "expansion_markets": ["Vietnam", "Philippines", "Indonesia"],
      "investment_budget": "5M_USD",
      "risk_assessment": true,
      "success_metrics": [
        "revenue_growth",
        "market_share",
        "customer_satisfaction",
        "operational_efficiency"
      ],
      "include_implementation_plan": true,
      "quarterly_reviews": true
    },
    "context": {
      "memory": "Current market position is strong in Thailand with 30% market share, ready for regional expansion",
      "retriever": [
        "current_business_performance",
        "market_opportunity_analysis",
        "competitive_landscape",
        "resource_capabilities",
        "regulatory_environment"
      ]
    },
    "business_id": "685e0265ee376ed320ab6609"
  }'
```

---

## 📋 **MCP Protocol Field Reference**

### **Required Fields**
- `description`: Human-readable task description
- `type`: Task type identifier (e.g., "financial_analysis", "content_generation")
- `params`: Task-specific parameters (object)

### **Optional Fields**
- `context`: MCP context object
  - `memory`: Persistent memory/context string
  - `retriever`: Array of data source identifiers
- `business_id`: Associated business identifier
- `callback_url`: Custom callback URL (auto-generated if not provided)

### **Common Task Types**
- `financial_analysis`: Financial performance analysis
- `market_research`: Market research and analysis
- `content_generation`: Content creation tasks
- `data_analysis`: Data analysis and insights
- `strategic_planning`: Strategic planning and roadmaps
- `competitive_analysis`: Competitive intelligence
- `risk_assessment`: Risk analysis and assessment
- `performance_review`: Performance evaluation tasks

---

## 🔄 Complete Workflow Example

Here's a complete example of creating a business, registering an agent, creating a task, and updating it via callback:

### 1. Create Business
```bash
curl -X POST "http://localhost:8000/api/v1/business/create" \
  -H "Content-Type: application/json" \
  -d '{
    "business_name": "Tech Startup XYZ",
    "description": "AI-powered business analytics platform",
    "business_type": "tech_startup",
    "location": "Bangkok, Thailand",
    "target_market": "Small to medium businesses",
    "competitors": ["Tableau", "Power BI"],
    "growth_goals": ["Expand to Southeast Asia", "Launch mobile app"]
  }'
```

### 2. Get Agent Types
```bash
curl -X GET "http://localhost:8000/api/v1/agents/types"
```

### 3. Register Agent
```bash
curl -X POST "http://localhost:8000/api/v1/agents/register" \
  -H "Content-Type: application/json" \
  -d '{
    "agent_name": "Business Analytics Agent",
    "agent_type": "analytics_agent",
    "endpoint_url": "http://localhost:3000/analytics",
    "api_key": "secret-key-123",
    "description": "Specialized in business analytics",
    "capabilities": ["data_analysis", "market_research", "insights"],
    "mcp_support": true
  }'
```

### 4. Create MCP Task
```bash
curl -X POST "http://localhost:8000/api/v1/agents/mcp/task" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Analyze market trends for premium tissue products in Thailand for 2024–2025.",
    "type": "market_analysis",
    "params": {
      "market_segment": "premium_tissue",
      "geographic_region": "Thailand",
      "time_period": "2024-2025"
    },
    "business_id": "685e0265ee376ed320ab6609",
    "llm_params": {
      "model": "gpt-4-turbo",
      "temperature": 0.3,
      "max_tokens": 1200
    },
    "output_preferences": {
      "format": "markdown",
      "audience": "executive_summary"
    },
    "tools": {
      "enable_web_search": true,
      "use_internal_market_data": true
    }
  }'
```

### 5. Update Task via Callback
```bash
# Use the callback_url from the task creation response
# Option 1: Wrapped format (with result_data)
curl -X POST "http://localhost:8000/api/v1/agents/mcp/callback?task_id=Njg1ZTA1MWVlODIwNTk1NTg2NjUyMGYx&token=2d5ab9441fd29d9aee12a19c4b53260acdd1c37665afef037a064edc677abd4c&expires_at=1750995758&signature=NDcwODdkOTZhNDU5MzlmNmVkYmU0NmFhNzU1OTJhMGJmNjBjODg3NmE4NGU5ZD" \
  -H "Content-Type: application/json" \
  -d '{
    "result_data": {
      "status": "completed",
      "output": {
        "text": "Competitive analysis completed",
        "data": {
          "market_share": {
            "Tableau": "35%",
            "Power BI": "45%",
            "Looker": "10%",
            "Others": "10%"
          },
          "key_differentiators": ["AI-powered insights", "SME focus", "Localization"],
          "recommendations": ["Focus on AI features", "Target underserved markets", "Build partnerships"]
        }
      },
      "execution_time": 15.2,
      "timestamp": "2025-06-27T03:00:00.000Z"
    }
  }'

# Option 2: Direct format (no wrapper - much simpler!)
curl -X POST "http://localhost:8000/api/v1/agents/mcp/callback?task_id=Njg1ZTA1MWVlODIwNTk1NTg2NjUyMGYx&token=2d5ab9441fd29d9aee12a19c4b53260acdd1c37665afef037a064edc677abd4c&expires_at=1750995758&signature=NDcwODdkOTZhNDU5MzlmNmVkYmU0NmFhNzU1OTJhMGJmNjBjODg3NmE4NGU5ZD" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Competitive analysis completed",
    "data": {
      "market_share": {
        "Tableau": "35%",
        "Power BI": "45%",
        "Looker": "10%",
        "Others": "10%"
      },
      "key_differentiators": ["AI-powered insights", "SME focus", "Localization"],
      "recommendations": ["Focus on AI features", "Target underserved markets", "Build partnerships"]
    },
    "execution_time": 15.2,
    "timestamp": "2025-06-27T03:00:00.000Z"
  }'
```

---

## 🔧 Additional Endpoints

### Get All Businesses
**GET** `/business/`
```bash
curl -X GET "http://localhost:8000/api/v1/business/?limit=10"
```

### Search Businesses
**GET** `/business/search`
```bash
curl -X GET "http://localhost:8000/api/v1/business/search?q=tech&business_type=tech_startup"
```

### Get All Tasks
**GET** `/agents/tasks`
```bash
curl -X GET "http://localhost:8000/api/v1/agents/tasks?status=completed&business_id=685e0265ee376ed320ab6609"
```

### Get Business Tasks
**GET** `/agents/business/{business_id}/tasks`
```bash
curl -X GET "http://localhost:8000/api/v1/agents/business/685e0265ee376ed320ab6609/tasks"
```

---

## 🔐 Security Features

- **Secure Callback URLs**: All callback URLs are signed with HMAC signatures
- **Token Expiration**: Callback tokens expire after 1 hour by default
- **Base64 Encoding**: Task IDs and signatures are base64 URL-safe encoded
- **API Key Support**: Agents can authenticate using API keys

---

## 📝 Notes

- All timestamps are in ISO 8601 format
- Task IDs are MongoDB ObjectIds converted to strings
- Callback URLs are automatically generated and secured
- The system supports both synchronous and asynchronous task processing
- Agent forwarding is logged in the `mcp_task_logs` collection for debugging

---

## 🐛 Troubleshooting

### Common Issues

1. **Agent Type Not Found**: Ensure the agent type exists in the system
2. **Invalid Callback URL**: Check that the callback URL parameters are correct
3. **Token Expired**: Generate a new task to get a fresh callback URL
4. **Database Connection**: Ensure MongoDB is running and accessible

### Debug Logs

The system logs forwarding attempts and responses to the `mcp_task_logs` collection. Check these logs for debugging agent communication issues. 