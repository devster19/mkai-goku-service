# Business Automation System

## Overview

The Business Automation System is an intelligent task management and monitoring system that automatically tracks business performance, executes scheduled tasks, and triggers re-analysis when goals aren't being met.

## Features

### 🎯 **Automated Goal Monitoring**
- Tracks business KPIs and performance metrics
- Monitors progress against set targets
- Automatically identifies when goals are at risk or behind schedule
- Triggers re-analysis when performance falls below expectations

### ⏰ **Scheduled Task Execution**
- **Daily Tasks**: Sales performance analysis, KPI monitoring
- **Weekly Tasks**: Market analysis, financial reviews, trend analysis
- **Monthly Tasks**: Strategic goal reviews, budget adjustments, brand monitoring

### 🤖 **Multi-Agent Task Distribution**
- Strategic Agent: Market analysis, goal reviews
- Financial Agent: Financial reviews, budget adjustments
- Sales Agent: Sales performance, customer feedback
- Analytics Agent: KPI monitoring, trend analysis
- Creative Agent: Marketing performance, brand monitoring

### 📊 **Real-time Dashboard**
- Visual progress tracking for all business goals
- Task execution status and history
- System-wide automation summary
- Recent activity monitoring

## How It Works

### 1. **Business Creation**
When a new business is created through the analysis system:
- Automated tasks are created for each agent based on business type
- Initial business goals are set (revenue, customers, profit margin, etc.)
- Task frequencies are adjusted based on business type (startups get more frequent monitoring)

### 2. **Task Execution**
- Tasks run automatically based on their configured frequency
- Each agent receives specific tasks with relevant parameters
- Results are used to update business goals and performance metrics

### 3. **Goal Monitoring**
- System continuously monitors goal achievement
- Progress is calculated as percentage of target value
- Status is updated: "on_track", "at_risk", "behind", or "achieved"

### 4. **Re-analysis Triggering**
When goals are not being met:
- System identifies the specific issues
- Triggers a new comprehensive business analysis
- Provides context about why re-analysis was needed

## Business Goals

### Common Goals (All Businesses)
- **Revenue Growth**: Target 1M THB annual revenue
- **Customer Acquisition**: Target 100 customers
- **Profit Margin**: Target 20% profit margin

### Business-Specific Goals
- **Tech Startups**: User growth (1000 active users)
- **Restaurants**: Daily customers (50 customers/day)
- **Retail Stores**: Inventory turnover (12x per year)

## API Endpoints

### Automation Management
- `GET /automation/summary` - Get system summary
- `GET /automation/business/{id}/tasks` - Get business tasks
- `GET /automation/business/{id}/goals` - Get business goals
- `POST /automation/business/{id}/check-goals` - Check goal achievement
- `POST /automation/start` - Start automation scheduler
- `POST /automation/stop` - Stop automation scheduler
- `POST /automation/task/{id}/execute` - Execute specific task

## Getting Started

### 1. **Start the Automation System**
```bash
cd openai-multi-agents
source venv/bin/activate
python3 start_automation.py
```

### 2. **Access the Dashboard**
- Navigate to any business in the main dashboard
- Click the Settings icon (⚙️) to access the automation dashboard
- Monitor tasks, goals, and system activity

### 3. **Manual Controls**
- **Start/Stop Automation**: Control the automation scheduler
- **Check Goals**: Manually trigger goal checking
- **Execute Tasks**: Run specific tasks on demand
- **Refresh Data**: Update dashboard information

## Task Types

### Strategic Agent Tasks
- **Market Analysis**: Weekly comprehensive market trend analysis
- **Goal Review**: Monthly strategic goal alignment review

### Financial Agent Tasks
- **Financial Review**: Weekly performance and projection analysis
- **Budget Adjustment**: Monthly performance-based budget updates

### Sales Agent Tasks
- **Sales Performance**: Daily sales pipeline and performance analysis
- **Customer Feedback**: Weekly comprehensive customer feedback collection

### Analytics Agent Tasks
- **KPI Monitoring**: Daily business metrics monitoring
- **Trend Analysis**: Weekly performance trend analysis

### Creative Agent Tasks
- **Marketing Performance**: Weekly campaign performance analysis
- **Brand Monitoring**: Monthly brand perception and awareness tracking

## Configuration

### Task Frequencies by Business Type
- **Tech Startups**: More frequent monitoring (daily/weekly)
- **Restaurants**: Standard monitoring (daily/weekly/monthly)
- **Retail Stores**: Standard monitoring (daily/weekly/monthly)
- **Consulting Firms**: Less frequent monitoring (weekly/monthly)

### Goal Thresholds
- **At Risk**: < 60% progress with < 60 days remaining
- **Behind**: < 80% progress with < 30 days remaining
- **Achieved**: 100% progress reached

## Monitoring and Alerts

### Automatic Alerts
- Goal status changes (on_track → at_risk → behind)
- Task execution failures
- Re-analysis triggers

### Dashboard Indicators
- Color-coded goal status
- Progress bars for each goal
- Task execution history
- System activity timeline

## Integration

### With Main System
- Automatically integrated with business analysis workflow
- Creates automation tasks when new businesses are analyzed
- Triggers re-analysis through the main processing pipeline

### With Agents
- Each agent receives automated task requests
- Tasks include business context and parameters
- Results update goal progress and trigger further actions

## Benefits

### For Business Owners
- **Continuous Monitoring**: Always know how your business is performing
- **Early Warning**: Get alerts before problems become critical
- **Automated Insights**: Regular analysis without manual effort
- **Goal Tracking**: Visual progress tracking for all objectives

### For Business Analysts
- **Automated Workflows**: Reduce manual monitoring tasks
- **Proactive Analysis**: Identify issues before they impact business
- **Comprehensive Coverage**: Monitor all aspects of business performance
- **Data-Driven Decisions**: Regular insights for strategic planning

## Troubleshooting

### Common Issues
1. **Tasks Not Executing**: Check if automation scheduler is running
2. **Goals Not Updating**: Verify agent responses include KPI data
3. **Re-analysis Not Triggering**: Check goal thresholds and deadlines

### Debug Commands
```bash
# Check automation status
curl http://localhost:5099/automation/summary

# Check specific business goals
curl http://localhost:5099/automation/business/{id}/goals

# Manually check goals
curl -X POST http://localhost:5099/automation/business/{id}/check-goals
```

## Future Enhancements

### Planned Features
- **Email Notifications**: Alert business owners of goal status changes
- **Custom Goals**: Allow users to set their own business goals
- **Advanced Analytics**: Machine learning for predictive goal achievement
- **Integration APIs**: Connect with external business systems
- **Mobile Dashboard**: Mobile app for automation monitoring

### Advanced Automation
- **Smart Scheduling**: AI-powered task frequency optimization
- **Predictive Re-analysis**: Proactive analysis based on trends
- **Cross-Business Insights**: Industry benchmarking and comparisons
- **Automated Recommendations**: AI-generated action plans

---

This automation system transforms the business analysis platform from a one-time analysis tool into a continuous business monitoring and optimization system, helping businesses achieve their goals through intelligent automation and proactive insights. 