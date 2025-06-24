# Quick Start Guide - Dynamic Business Input System

This guide will help you get started with the dynamic business input system that supports any type of business, not just coffee shops.

## 🚀 Quick Setup

### 1. Start the Multi-Agent System

```bash
# Start all AI agents
python start_agents.py
```

Wait for all agents to start (you'll see "✓ All agents started successfully!")

### 2. Use the Web Interface (Recommended)

```bash
# Start the web form server
python serve_form.py
```

Your browser will automatically open to `http://localhost:8080/business_input_form.html`

### 3. Fill Out the Form

1. **Business Name**: Enter your business name
2. **Business Type**: Select from dropdown (coffee_shop, restaurant, tech_startup, etc.)
3. **Location**: Enter city and country
4. **Description**: Describe your business, products/services
5. **Target Market**: Describe your target customers
6. **Additional Fields**: Fill in industry, business model, investment amount, etc.
7. **Competitors**: Add your main competitors
8. **Growth Goals**: Add your business goals
9. **Submit**: Click "Analyze My Business"

### 4. View Results

The system will analyze your business using 8 specialized AI agents and display:
- Strategic Plan
- Financial Analysis
- Creative/Marketing Strategy
- Sales Strategy
- SWOT Analysis
- Business Model Canvas
- Analytics Summary
- Overall Recommendations

## 🧪 Testing Different Business Types

### Test with Pre-built Examples

```bash
# Test coffee shop
python test_system.py coffee_shop

# Test tech startup
python test_system.py tech_startup

# Test restaurant
python test_system.py restaurant

# Test e-commerce
python test_system.py ecommerce

# Test all business types
python test_system.py all
```

### Demo Script

```bash
# Run demo for all business types
python demo_dynamic_input.py

# Run demo for specific business type
python demo_dynamic_input.py tech_startup
```

## 📊 API Usage

### Direct API Call

```bash
curl -X POST "http://localhost:5099/process-business" \
     -H "Content-Type: application/json" \
     -d '{
       "business_name": "My Tech Startup",
       "business_type": "tech_startup",
       "location": "San Francisco, CA",
       "description": "AI-powered business automation platform",
       "target_market": "Small businesses looking to automate tasks",
       "competitors": ["Zapier", "Automation Anywhere"],
       "growth_goals": ["Reach 1000 customers", "Expand to Europe"],
       "initial_investment": 200000.0,
       "team_size": 15,
       "business_model": "b2b",
       "industry": "technology"
     }'
```

### Python Script

```python
import httpx
import asyncio

async def analyze_business():
    business_data = {
        "business_name": "My Restaurant",
        "business_type": "restaurant",
        "location": "New York, NY",
        "description": "Modern fusion restaurant",
        "target_market": "Food enthusiasts aged 25-45",
        "competitors": ["Competitor A", "Competitor B"],
        "growth_goals": ["Open second location", "Launch catering"],
        "initial_investment": 300000.0,
        "team_size": 25,
        "business_model": "b2c",
        "industry": "food_beverage"
    }
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:5099/process-business",
            json=business_data
        )
        
        if response.status_code == 200:
            result = response.json()
            print("Analysis completed!")
            print(f"Success probability: {result['analytics_summary']['success_probability']['overall_success_rate']}")
        else:
            print(f"Error: {response.status_code}")

asyncio.run(analyze_business())
```

## 🏢 Supported Business Types

The system supports any business type, including:

- **Coffee Shops & Cafes**
- **Restaurants**
- **Retail Stores**
- **Technology Startups**
- **E-commerce Platforms**
- **Consulting Firms**
- **Manufacturing**
- **Healthcare**
- **Education**
- **Real Estate**
- **Fitness & Gym**
- **Beauty Salons**
- **Automotive**
- **And more...**

## 📋 Required Fields

### Minimum Required
- `business_name`: Your business name
- `business_type`: Type of business
- `location`: City, country
- `description`: Business description
- `target_market`: Target customers
- `competitors`: List of competitors
- `growth_goals`: List of growth goals

### Optional Fields
- `initial_investment`: Investment amount
- `team_size`: Number of employees
- `unique_value_proposition`: What makes you unique
- `business_model`: b2c, b2b, marketplace, etc.
- `industry`: food_beverage, technology, retail, etc.
- `market_size`: local, regional, national, international
- `technology_requirements`: List of tech needs
- `regulatory_requirements`: List of regulations

## 🔍 Understanding Results

### Strategic Plan
- Market analysis and positioning
- Competitive advantages
- Growth strategy
- Risk assessment

### Financial Analysis
- Revenue projections
- Funding requirements
- Pricing strategy
- Break-even analysis

### Creative Analysis
- Brand identity
- Marketing campaigns
- Visual design
- Content strategy

### Sales Strategy
- Target customer segments
- Sales channels
- Customer acquisition
- Sales metrics

### SWOT Analysis
- Strengths, Weaknesses, Opportunities, Threats

### Business Model Canvas
- Key partners, activities, resources
- Value propositions
- Customer relationships, segments
- Channels, cost structure, revenue streams

### Analytics Summary
- Success probability
- Risk assessment
- Key insights

## 🛠️ Troubleshooting

### Common Issues

1. **Agents not starting**
   ```bash
   # Check if ports are available
   lsof -i :5001-5008
   # Kill processes if needed
   pkill -f "python.*agent"
   ```

2. **OpenAI API errors**
   ```bash
   # Check your .env file
   cat .env
   # Make sure OPENAI_API_KEY is set
   ```

3. **Form not loading**
   ```bash
   # Check if form server is running
   curl http://localhost:8080/business_input_form.html
   ```

4. **Analysis taking too long**
   - Check agent health: `curl http://localhost:5099/health`
   - Increase timeout in your client
   - Check OpenAI API rate limits

### Health Checks

```bash
# Core agent
curl http://localhost:5099/health

# Individual agents
curl http://localhost:5001/health
curl http://localhost:5002/health
curl http://localhost:5003/health
curl http://localhost:5004/health
curl http://localhost:5005/health
curl http://localhost:5006/health
curl http://localhost:5007/health
curl http://localhost:5008/health
```

## 📚 Next Steps

1. **Customize Analysis**: Modify agent prompts for your specific needs
2. **Add New Business Types**: Extend the system with industry-specific analysis
3. **Integrate with External Data**: Connect to market research APIs
4. **Build Custom UI**: Create your own frontend interface
5. **Scale the System**: Deploy to production with proper infrastructure

## 🆘 Getting Help

- Check the main README.md for detailed documentation
- Review API docs at `http://localhost:5099/docs`
- Test with the provided examples
- Check agent logs for detailed error messages

---

**Happy Business Analysis! 🚀** 