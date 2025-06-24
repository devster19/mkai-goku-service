# Quick Start Guide

## 🚀 How to Run the Multi-Agent Business Analysis System

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Internet connection

### Step 1: Setup (One-time)
```bash
# Run the setup script
python setup.py
```

This will:
- Check Python version
- Create virtual environment
- Install dependencies
- Create .env file from template
- Set up directories

### Step 2: Configure OpenAI API Key
Edit the `.env` file and replace `your_openai_api_key_here` with your actual OpenAI API key:

```env
OPENAI_API_KEY=sk-your-actual-api-key-here
```

### Step 3: Start the System
```bash
# Start all agents
python start_agents.py
```

This will start:
- Core Agent (Port 5099) - Main orchestrator
- Strategic Agent (Port 5001) - Business strategy
- Creative Agent (Port 5002) - Marketing & branding
- Financial Agent (Port 5003) - Financial analysis
- Sales Agent (Port 5004) - Sales strategy
- Manager Agent (Port 5005) - Process coordination
- Analytics Agent (Port 5006) - Data analysis
- SWOT Agent (Port 5007) - SWOT analysis
- Business Model Canvas Agent (Port 5008) - Business model

### Step 4: Test the System
```bash
# In a new terminal, test the system
python test_system.py
```

### Step 5: Use the API
Send a business analysis request:

```bash
curl -X POST "http://localhost:5099/process-business" \
     -H "Content-Type: application/json" \
     -d '{
       "business_name": "ร้านกาแฟสดใจดี",
       "location": "กรุงเทพมหานคร",
       "competitors": ["ร้านกาแฟ Amazon", "ร้านกาแฟ All Cafe"],
       "growth_goals": ["เพิ่มยอดขาย 50% ภายใน 1 ปี", "ขยายสาขาใหม่"]
     }'
```

### Step 6: View Results
- **API Documentation**: http://localhost:5099/docs
- **Health Check**: http://localhost:5099/health
- **Individual Agent Health**: http://localhost:5001/health (Strategic), etc.

## 📊 What You'll Get

The system will provide comprehensive business analysis including:

1. **Strategic Plan** - Market positioning, growth strategy, competitive analysis
2. **SWOT Analysis** - Strengths, Weaknesses, Opportunities, Threats
3. **Business Model Canvas** - All 9 building blocks of the business model
4. **Creative Analysis** - Brand identity, marketing campaigns, visual design
5. **Financial Analysis** - Revenue projections, funding requirements, pricing
6. **Sales Strategy** - Customer segments, sales channels, acquisition strategies
7. **Analytics Summary** - Cross-functional insights and recommendations

## 🔧 Troubleshooting

### Common Issues:

1. **Port already in use**
   ```bash
   # Check what's using the ports
   lsof -i :5099-5008
   # Kill processes if needed
   kill -9 <PID>
   ```

2. **OpenAI API errors**
   - Check your API key in `.env` file
   - Ensure you have sufficient credits
   - Check internet connection

3. **Dependencies not found**
   ```bash
   # Reinstall dependencies
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Agents not starting**
   - Check if all agent files exist in `agents/` directory
   - Ensure Python virtual environment is activated
   - Check logs for specific error messages

### Manual Agent Testing:
```bash
# Test individual agents
curl http://localhost:5001/health  # Strategic Agent
curl http://localhost:5007/health  # SWOT Agent
curl http://localhost:5008/health  # Business Model Canvas Agent
```

## 🛑 Stopping the System
Press `Ctrl+C` in the terminal where you ran `start_agents.py` to stop all agents gracefully.

## 📈 Performance
- **Response Time**: 2-3 minutes for complete analysis
- **Concurrent Requests**: Supports multiple simultaneous requests
- **Memory Usage**: ~500MB total for all agents
- **CPU Usage**: Moderate during analysis, low when idle

## 🔄 Workflow
1. User sends business data to Core Agent
2. Core Agent orchestrates analysis across all specialized agents
3. Agents process in parallel where possible
4. Results are aggregated and returned to user
5. Comprehensive business analysis with actionable recommendations

## 📝 Example Output
The system returns a structured JSON response with:
- Strategic analysis and positioning
- SWOT analysis with action plans
- Complete Business Model Canvas
- Creative marketing strategies
- Financial projections and planning
- Sales and customer acquisition strategies
- Cross-functional insights and recommendations

## 🎯 Next Steps
- Customize agent prompts for your specific business domain
- Add more specialized agents as needed
- Integrate with external data sources
- Deploy to production environment
- Add authentication and rate limiting

For detailed documentation, see `README.md`. 