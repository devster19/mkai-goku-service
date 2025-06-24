# Multi-Agent Business Analysis System

A sophisticated multi-agent system that provides comprehensive business analysis using AI-powered agents specialized in different business domains.

## 🎯 Overview

This system implements a Model Context Protocol (MCP) based multi-agent architecture where specialized AI agents collaborate to provide comprehensive business analysis. The system is designed to analyze business opportunities, particularly focused on the Thai market and coffee shop businesses.

## 🏗️ Architecture

```
User Input (HTTP POST) → FastAPI Core Agent (Python)
        |
        v
Core Agent uses MCP Client to:
   - Delegate tasks to Strategic Agent (or itself)
   - Strategic Agent delegates to Creative, Financial, Sales Agents
   - Manager Agent triggers Analytics periodically
        |
        v
Receive responses from agents via MCP
        |
        v
Aggregate results and respond back to user
```

### Agent Specializations

1. **Strategic Agent** (Port 8001) - Business strategy and market positioning
2. **Creative Agent** (Port 8002) - Marketing, branding, and creative strategy
3. **Financial Agent** (Port 8003) - Financial analysis, projections, and planning
4. **Sales Agent** (Port 8004) - Sales strategy and customer acquisition
5. **Manager Agent** (Port 8005) - Process coordination and management
6. **Analytics Agent** (Port 8006) - Comprehensive data analysis and insights
7. **Core Agent** (Port 8000) - Main orchestrator and API gateway

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- OpenAI API key
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd openai-multi-agents
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp config.env.example .env
   # Edit .env file and add your OpenAI API key
   ```

5. **Start the system**
   ```bash
   python start_agents.py
   ```

### Testing the System

Run the test script to verify everything is working:

```bash
python test_system.py
```

## 📊 API Usage

### Main Endpoint

**POST** `/process-business`

Analyzes business data and returns comprehensive analysis.

#### Request Body

```json
{
  "business_name": "ร้านกาแฟสดใจดี",
  "location": "กรุงเทพมหานคร",
  "competitors": ["ร้านกาแฟ Amazon", "ร้านกาแฟ All Cafe"],
  "growth_goals": ["เพิ่มยอดขาย 50% ภายใน 1 ปี", "ขยายสาขาใหม่"]
}
```

#### Response Structure

```json
{
  "business_name": "ร้านกาแฟสดใจดี",
  "timestamp": "2024-01-15T10:30:00",
  "strategic_plan": {
    "market_analysis": {...},
    "competitive_positioning": {...},
    "growth_strategy": {...},
    "risk_assessment": {...},
    "key_recommendations": [...]
  },
  "creative_analysis": {
    "brand_identity": {...},
    "marketing_campaigns": [...],
    "visual_design": {...},
    "recommendations": [...]
  },
  "financial_analysis": {
    "financial_projections": {...},
    "funding_requirements": {...},
    "pricing_strategy": {...},
    "recommendations": [...]
  },
  "sales_strategy": {
    "target_customer_segments": {...},
    "sales_channels": {...},
    "customer_acquisition_strategies": {...},
    "recommendations": [...]
  },
  "analytics_summary": {
    "success_probability": {...},
    "risk_assessment": {...},
    "key_insights": [...]
  },
  "overall_recommendations": [...]
}
```

### Health Check

**GET** `/health`

Returns system health status.

### API Documentation

Visit `http://localhost:8000/docs` for interactive API documentation.

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here

# Agent URLs (default configuration)
STRATEGIC_AGENT_URL=http://localhost:8001
CREATIVE_AGENT_URL=http://localhost:8002
FINANCIAL_AGENT_URL=http://localhost:8003
SALES_AGENT_URL=http://localhost:8004
MANAGER_AGENT_URL=http://localhost:8005
ANALYTICS_AGENT_URL=http://localhost:8006

# Core Agent Configuration
CORE_AGENT_PORT=8000
CORE_AGENT_HOST=0.0.0.0
```

## 🧪 Testing

### Manual Testing with curl

```bash
curl -X POST "http://localhost:8000/process-business" \
     -H "Content-Type: application/json" \
     -d '{
       "business_name": "ร้านกาแฟสดใจดี",
       "location": "กรุงเทพมหานคร",
       "competitors": ["ร้านกาแฟ Amazon", "ร้านกาแฟ All Cafe"],
       "growth_goals": ["เพิ่มยอดขาย 50% ภายใน 1 ปี", "ขยายสาขาใหม่"]
     }'
```

### Automated Testing

```bash
python test_system.py
```

## 📁 Project Structure

```
openai-multi-agents/
├── main.py                 # Core Agent (FastAPI application)
├── start_agents.py         # Startup script for all agents
├── test_system.py          # System testing script
├── requirements.txt        # Python dependencies
├── config.env.example      # Environment configuration template
├── README.md              # This file
└── agents/                # Individual agent servers
    ├── __init__.py
    ├── strategic_agent.py  # Strategic analysis agent
    ├── creative_agent.py   # Creative/marketing agent
    ├── financial_agent.py  # Financial analysis agent
    ├── sales_agent.py      # Sales strategy agent
    ├── manager_agent.py    # Process management agent
    └── analytics_agent.py  # Data analytics agent
```

## 🔄 Workflow

1. **User submits business data** via HTTP POST to Core Agent
2. **Core Agent validates input** and creates request ID
3. **Strategic Agent analyzes** business strategy and positioning
4. **Parallel processing** of Creative, Financial, and Sales agents
5. **Analytics Agent synthesizes** all outputs for comprehensive insights
6. **Core Agent aggregates** all results and generates overall recommendations
7. **Response returned** to user with complete business analysis

## 🎨 Features

### Strategic Analysis
- Market positioning strategy
- Competitive advantage analysis
- Growth strategy recommendations
- Risk assessment and mitigation
- Implementation timeline

### Creative Analysis
- Brand identity development
- Marketing campaign ideas
- Visual design suggestions
- Content marketing strategy
- Social media approach

### Financial Analysis
- Revenue projections and forecasts
- Funding requirements and sources
- Cost structure analysis
- Pricing strategy recommendations
- Break-even analysis

### Sales Strategy
- Target customer segmentation
- Sales channels and distribution
- Customer acquisition strategies
- Retention and loyalty programs
- Partnership opportunities

### Analytics Integration
- Cross-functional insights
- Success probability analysis
- Risk assessment
- Resource optimization
- Implementation priorities

## 🛠️ Development

### Adding New Agents

1. Create a new agent file in the `agents/` directory
2. Implement the MCP message interface
3. Add agent configuration to `start_agents.py`
4. Update the Core Agent to include the new agent

### Customizing Agent Logic

Each agent can be customized by modifying:
- OpenAI prompts and system messages
- Analysis structure and output format
- Business logic and calculations
- Integration with external APIs

### Extending the System

The modular architecture allows for:
- Adding new business domains
- Integrating with external data sources
- Implementing caching and optimization
- Adding authentication and authorization
- Scaling to multiple instances

## 🔒 Security Considerations

- Store API keys securely in environment variables
- Implement rate limiting for API endpoints
- Add authentication for production use
- Validate and sanitize all input data
- Monitor system logs for suspicious activity

## 📈 Performance

- **Response Time**: 2-3 minutes for complete analysis
- **Concurrent Requests**: Supports multiple simultaneous requests
- **Scalability**: Can be scaled horizontally by adding agent instances
- **Reliability**: Fallback responses when OpenAI API is unavailable

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For issues and questions:
1. Check the API documentation at `http://localhost:8000/docs`
2. Review the test output for debugging information
3. Check agent health endpoints for individual agent status
4. Review system logs for detailed error information

## 🔮 Future Enhancements

- [ ] Database integration for storing analysis results
- [ ] Real-time market data integration
- [ ] Advanced analytics and machine learning models
- [ ] Web-based dashboard for results visualization
- [ ] Multi-language support
- [ ] Integration with business planning tools
- [ ] Automated report generation
- [ ] Mobile application support 