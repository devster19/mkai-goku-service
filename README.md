# Multi-Agent Business Analysis System

A sophisticated multi-agent system that provides comprehensive business analysis using AI-powered agents specialized in different business domains.

## 🎯 Overview

This system implements a Model Context Protocol (MCP) based multi-agent architecture where specialized AI agents collaborate to provide comprehensive business analysis. The system now supports **dynamic business input** for any type of business, not just coffee shops.

## 🆕 New Features

### Modern React Frontend
- **React + Vite**: Fast, modern frontend built with React 18 and Vite
- **Tailwind CSS**: Beautiful, responsive design with utility-first CSS
- **Interactive Dashboard**: View and manage all business analyses
- **Dynamic Forms**: Comprehensive business input form with real-time validation
- **Results Viewer**: Interactive results display with tabbed sections
- **Mobile Responsive**: Optimized for all device sizes

### Dynamic Business Input
- **Web Interface**: User-friendly React form for business input
- **Multiple Business Types**: Support for coffee shops, restaurants, tech startups, e-commerce, and more
- **Comprehensive Data Model**: Rich business information including industry, business model, technology requirements, etc.
- **Flexible Analysis**: AI agents adapt their analysis based on business type and characteristics

### Business Types Supported
- Coffee Shops & Cafes
- Restaurants
- Retail Stores
- Technology Startups
- E-commerce Platforms
- Consulting Firms
- Manufacturing
- Healthcare
- Education
- Real Estate
- Fitness & Gym
- Beauty Salons
- Automotive
- And more...

## 🏗️ Architecture

```
React Frontend (Port 5173) → FastAPI Core Agent (Port 8000)
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
Aggregate results and respond back to frontend
```

### Agent Specializations

1. **Strategic Agent** (Port 5001) - Business strategy and market positioning
2. **Creative Agent** (Port 5002) - Marketing, branding, and creative strategy
3. **Financial Agent** (Port 5003) - Financial analysis, projections, and planning
4. **Sales Agent** (Port 5004) - Sales strategy and customer acquisition
5. **Manager Agent** (Port 5005) - Process coordination and management
6. **Analytics Agent** (Port 5006) - Comprehensive data analysis and insights
7. **SWOT Agent** (Port 5007) - SWOT analysis
8. **Business Model Canvas Agent** (Port 5008) - Business model canvas creation
9. **Core Agent** (Port 8000) - Main orchestrator and API gateway

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+
- OpenAI API key
- Virtual environment (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd openai-multi-agents
   ```

2. **Set up Python backend**
   ```bash
   # Create and activate virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   
   # Install dependencies
   pip install -r requirements.txt
   
   # Configure environment
   cp config.env.example .env
   # Edit .env file and add your OpenAI API key
   ```

3. **Set up React frontend**
   ```bash
   # Navigate to frontend directory
   cd frontend
   
   # Install dependencies
   npm install
   ```

4. **Start the system**
   ```bash
   # Start the Python backend (from the main directory)
   python start_agents.py
   
   # In a new terminal, start the React frontend
   cd frontend
   npm run dev
   ```

5. **Access the application**
   - Frontend: `http://localhost:5173`
   - Backend API: `http://localhost:8000`

### Using the Web Interface

1. **Open your browser** and go to `http://localhost:5173`

2. **Dashboard**: View all your business analyses, search, and manage them

3. **Create New Analysis**: Click "New Analysis" to fill out the comprehensive business form

4. **View Results**: Click on any analysis to view detailed results with interactive tabs

### Testing the System

#### Test Default Business (Coffee Shop)
```bash
python test_system.py
```

#### Test Specific Business Types
```bash
python test_system.py coffee_shop
python test_system.py tech_startup
python test_system.py restaurant
python test_system.py ecommerce
```

#### Test All Business Types
```bash
python test_system.py all
```

## 📊 API Usage

### Main Endpoint

**POST** `/process-business`

Analyzes business data and returns comprehensive analysis.

#### Request Body (Enhanced)

```json
{
  "business_name": "TechFlow Solutions",
  "business_type": "tech_startup",
  "location": "San Francisco, CA",
  "description": "AI-powered workflow automation platform for small businesses",
  "target_market": "Small to medium businesses (10-500 employees) looking to automate repetitive tasks",
  "competitors": ["Zapier", "Microsoft Power Automate", "Automation Anywhere"],
  "growth_goals": ["Reach 1000 customers in 12 months", "Expand to European market"],
  "initial_investment": 200000.0,
  "team_size": 15,
  "unique_value_proposition": "No-code AI automation specifically designed for small businesses",
  "business_model": "b2b",
  "industry": "technology",
  "market_size": "national",
  "technology_requirements": ["Cloud infrastructure", "AI/ML platform", "Mobile app development"],
  "regulatory_requirements": ["Data protection compliance", "SOC 2 certification"]
}
```

#### Response Structure

```json
{
  "business_name": "TechFlow Solutions",
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
  "swot_analysis": {
    "strengths": {...},
    "weaknesses": {...},
    "opportunities": {...},
    "threats": {...}
  },
  "business_model_canvas": {
    "key_partners": [...],
    "key_activities": [...],
    "value_propositions": [...],
    "customer_relationships": [...],
    "customer_segments": [...],
    "key_resources": [...],
    "channels": [...],
    "cost_structure": {...},
    "revenue_streams": [...]
  },
  "analytics_summary": {
    "market_size_estimate": {...},
    "competitive_landscape": {...},
    "trend_analysis": {...},
    "risk_factors": [...],
    "success_indicators": [...]
  },
  "overall_recommendations": [
    "Focus on building strong partnerships with small business software providers",
    "Develop a freemium model to attract initial users",
    "Invest in customer success and support infrastructure",
    "Consider strategic partnerships for market expansion"
  ]
}
```

### Additional Endpoints

- **GET** `/get-all-businesses` - Retrieve all business analyses
- **GET** `/search-businesses` - Search businesses by name or type
- **GET** `/get-analysis/{business_id}` - Get specific analysis results
- **DELETE** `/delete-business/{business_id}` - Delete a business analysis
- **GET** `/health` - Health check endpoint

## 🎨 Frontend Features

### Dashboard
- **Business Grid**: View all analyses in a responsive card layout
- **Search & Filter**: Find businesses by name, type, or other criteria
- **Statistics**: Overview of total analyses, recent activity, etc.
- **Actions**: View details, delete analyses, create new ones

### Business Form
- **Dynamic Fields**: Add/remove competitors, goals, requirements
- **Validation**: Real-time form validation with error messages
- **Business Types**: Dropdown selection for different business categories
- **Rich Input**: Text areas, number inputs, multi-select fields

### Results Viewer
- **Tabbed Interface**: Organized sections for different analysis types
- **Interactive Charts**: Visual representation of data (future enhancement)
- **Export Options**: Download results as PDF or JSON (future enhancement)
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🔧 Development

### Frontend Development
```bash
cd frontend
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
```

### Backend Development
```bash
# Start individual agents for development
python agents/strategic_agent.py
python agents/creative_agent.py
# ... etc

# Or start all agents together
python start_agents.py
```

### Adding New Features
1. **Frontend**: Add new components in `frontend/src/components/`
2. **Backend**: Add new endpoints in `main.py`
3. **Agents**: Create new agent files in `agents/` directory

## 📁 Project Structure

```
mkai-multiagents/
├── openai-multi-agents/          # Python backend
│   ├── agents/                   # Individual agent modules
│   ├── main.py                   # FastAPI application
│   ├── database.py               # Database operations
│   ├── requirements.txt          # Python dependencies
│   └── README.md                 # Backend documentation
├── frontend/                     # React frontend
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── App.jsx              # Main app component
│   │   └── index.css            # Global styles
│   ├── package.json             # Node.js dependencies
│   └── README.md                # Frontend documentation
└── README.md                    # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Check the documentation in each directory
- Review the API endpoints
- Test with the provided examples 