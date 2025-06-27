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
  "description": "string",             // REQUIRED: Task description
  "type": "string",                    // REQUIRED: Task type (e.g., "content_generation", "analysis")
  "params": {},                        // REQUIRED: Task parameters
  "context": {                         // OPTIONAL: MCP context
    "memory": "string",
    "retriever": ["string"]
  },
  "callback_url": "string",            // OPTIONAL: Custom callback URL
  "business_id": "string"              // OPTIONAL: Associated business ID
}
```

#### Example Request
```bash
curl -X POST "http://localhost:8000/api/v1/agents/mcp/task" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Analyze market trends for tissue products",
    "type": "market_analysis",
    "params": {
      "market_segment": "premium_tissue",
      "geographic_region": "Thailand",
      "time_period": "2024-2025"
    },
    "business_id": "685e0265ee376ed320ab6609"
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

### Update Task via Callback URL

When a task is created, a secure callback URL is generated. Agents can use this URL to update task results.

#### Callback URL Format
```
http://localhost:8000/api/v1/agents/mcp/callback?task_id={encoded_task_id}&token={token}&expires_at={expires_at}&signature={signature}
```

#### Request Body for Callback
```json
{
  "status": "completed",               // REQUIRED: Task status
  "output": {                          // OPTIONAL: Task output
    "text": "string",
    "images": [
      {
        "url": "string",
        "caption": "string",
        "alt_text": "string",
        "type": "image"
      }
    ],
    "links": [
      {
        "title": "string",
        "url": "string",
        "description": "string"
      }
    ],
    "files": [
      {
        "filename": "string",
        "url": "string",
        "size": 0,
        "mime_type": "string"
      }
    ],
    "data": {},                        // Structured data
    "html": "string",                  // HTML content
    "markdown": "string"               // Markdown content
  },
  "context_update": {                  // OPTIONAL: Context updates
    "memory": "string",
    "tags": ["string"],
    "metadata": {}
  },
  "execution_time": 2.5,               // OPTIONAL: Execution time in seconds
  "error_message": "string",           // OPTIONAL: Error message if failed
  "timestamp": "2025-06-27T02:45:00.000Z"  // OPTIONAL: Timestamp
}
```

#### Example Callback Request
```bash
curl -X POST "http://localhost:8000/api/v1/agents/mcp/callback?task_id=Njg1ZTA1MWVlODIwNTk1NTg2NjUyMGYx&token=2d5ab9441fd29d9aee12a19c4b53260acdd1c37665afef037a064edc677abd4c&expires_at=1750995758&signature=NDcwODdkOTZhNDU5MzlmNmVkYmU0NmFhNzU1OTJhMGJmNjBjODg3NmE4NGU5ZD" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "completed",
    "output": {
      "text": "Market analysis completed successfully",
      "data": {
        "market_size": "1.2B THB",
        "growth_rate": "8.5%",
        "key_insights": ["Premium segment growing", "Online sales opportunity"]
      }
    },
    "execution_time": 2.5,
    "timestamp": "2025-06-27T02:45:00.000Z"
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
  "status": "completed",
  "result": {
    "market_size": "1.2B THB",
    "growth_rate": "8.5%",
    "key_insights": ["Premium segment growing", "Online sales opportunity"]
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
    "description": "Analyze competitive landscape for business analytics platform",
    "type": "competitive_analysis",
    "params": {
      "competitors": ["Tableau", "Power BI", "Looker"],
      "market_focus": "SME segment",
      "geographic_region": "Southeast Asia"
    },
    "business_id": "685e0265ee376ed320ab6609"
  }'
```

### 5. Update Task via Callback
```bash
# Use the callback_url from the task creation response
curl -X POST "http://localhost:8000/api/v1/agents/mcp/callback?task_id=Njg1ZTA1MWVlODIwNTk1NTg2NjUyMGYx&token=2d5ab9441fd29d9aee12a19c4b53260acdd1c37665afef037a064edc677abd4c&expires_at=1750995758&signature=NDcwODdkOTZhNDU5MzlmNmVkYmU0NmFhNzU1OTJhMGJmNjBjODg3NmE4NGU5ZD" \
  -H "Content-Type: application/json" \
  -d '{
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