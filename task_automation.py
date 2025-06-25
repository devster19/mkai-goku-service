# Task Automation System

import asyncio
import schedule
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import httpx
import json
from dataclasses import dataclass
from enum import Enum
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TaskFrequency(Enum):
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class AutomatedTask:
    business_id: str
    business_name: str
    agent_type: str
    task_type: str
    frequency: TaskFrequency
    last_executed: Optional[datetime] = None
    next_execution: Optional[datetime] = None
    status: TaskStatus = TaskStatus.PENDING
    parameters: Dict[str, Any] = None
    results: Dict[str, Any] = None


@dataclass
class BusinessGoal:
    business_id: str
    goal_type: str
    target_value: float
    current_value: float
    deadline: datetime
    status: str  # "on_track", "at_risk", "behind", "achieved"
    last_updated: datetime


class TaskAutomationEngine:
    """Automated task management and business monitoring system"""

    def __init__(self):
        self.tasks: List[AutomatedTask] = []
        self.business_goals: Dict[str, List[BusinessGoal]] = {}
        self.mcp_client = httpx.AsyncClient(timeout=30.0)
        self.running = False

        # Agent task templates
        self.agent_tasks = {
            "strategic": {
                "market_analysis": {
                    "description": "Analyze market trends and competitive landscape",
                    "frequency": TaskFrequency.WEEKLY,
                    "parameters": {"analysis_depth": "comprehensive"},
                },
                "goal_review": {
                    "description": "Review and adjust strategic goals",
                    "frequency": TaskFrequency.MONTHLY,
                    "parameters": {"review_type": "strategic_alignment"},
                },
            },
            "financial": {
                "financial_review": {
                    "description": "Review financial performance and projections",
                    "frequency": TaskFrequency.WEEKLY,
                    "parameters": {"review_type": "performance_analysis"},
                },
                "budget_adjustment": {
                    "description": "Adjust budgets based on performance",
                    "frequency": TaskFrequency.MONTHLY,
                    "parameters": {"adjustment_type": "performance_based"},
                },
            },
            "sales": {
                "sales_performance": {
                    "description": "Analyze sales performance and pipeline",
                    "frequency": TaskFrequency.DAILY,
                    "parameters": {"analysis_type": "daily_performance"},
                },
                "customer_feedback": {
                    "description": "Collect and analyze customer feedback",
                    "frequency": TaskFrequency.WEEKLY,
                    "parameters": {"feedback_type": "comprehensive"},
                },
            },
            "analytics": {
                "kpi_monitoring": {
                    "description": "Monitor key performance indicators",
                    "frequency": TaskFrequency.DAILY,
                    "parameters": {"kpi_type": "business_metrics"},
                },
                "trend_analysis": {
                    "description": "Analyze business trends and patterns",
                    "frequency": TaskFrequency.WEEKLY,
                    "parameters": {"trend_type": "performance_trends"},
                },
            },
            "creative": {
                "marketing_performance": {
                    "description": "Analyze marketing campaign performance",
                    "frequency": TaskFrequency.WEEKLY,
                    "parameters": {"campaign_type": "all_active"},
                },
                "brand_monitoring": {
                    "description": "Monitor brand perception and awareness",
                    "frequency": TaskFrequency.MONTHLY,
                    "parameters": {"monitoring_type": "brand_health"},
                },
            },
        }

    async def create_business_automation(
        self, business_id: str, business_name: str, business_type: str
    ):
        """Create automated tasks for a new business"""
        logger.info(f"Creating automation tasks for business: {business_name}")

        # Create tasks for each agent based on business type
        for agent_type, tasks in self.agent_tasks.items():
            for task_type, task_config in tasks.items():
                # Adjust frequency based on business type
                frequency = self._adjust_frequency_for_business_type(
                    task_config["frequency"], business_type
                )

                task = AutomatedTask(
                    business_id=business_id,
                    business_name=business_name,
                    agent_type=agent_type,
                    task_type=task_type,
                    frequency=frequency,
                    next_execution=self._calculate_next_execution(frequency),
                    parameters=task_config["parameters"],
                )

                self.tasks.append(task)

        # Create initial business goals
        self._create_initial_goals(business_id, business_type)

        logger.info(
            f"Created {len(self.agent_tasks) * len(self.agent_tasks['strategic'])} tasks for {business_name}"
        )

    def _adjust_frequency_for_business_type(
        self, base_frequency: TaskFrequency, business_type: str
    ) -> TaskFrequency:
        """Adjust task frequency based on business type"""
        frequency_adjustments = {
            "tech_startup": {
                TaskFrequency.DAILY: TaskFrequency.DAILY,
                TaskFrequency.WEEKLY: TaskFrequency.DAILY,
                TaskFrequency.MONTHLY: TaskFrequency.WEEKLY,
            },
            "restaurant": {
                TaskFrequency.DAILY: TaskFrequency.DAILY,
                TaskFrequency.WEEKLY: TaskFrequency.WEEKLY,
                TaskFrequency.MONTHLY: TaskFrequency.MONTHLY,
            },
            "retail_store": {
                TaskFrequency.DAILY: TaskFrequency.DAILY,
                TaskFrequency.WEEKLY: TaskFrequency.WEEKLY,
                TaskFrequency.MONTHLY: TaskFrequency.MONTHLY,
            },
            "consulting_firm": {
                TaskFrequency.DAILY: TaskFrequency.WEEKLY,
                TaskFrequency.WEEKLY: TaskFrequency.WEEKLY,
                TaskFrequency.MONTHLY: TaskFrequency.MONTHLY,
            },
        }

        return frequency_adjustments.get(business_type, {}).get(
            base_frequency, base_frequency
        )

    def _calculate_next_execution(self, frequency: TaskFrequency) -> datetime:
        """Calculate next execution time based on frequency"""
        now = datetime.now()

        if frequency == TaskFrequency.DAILY:
            return now + timedelta(days=1)
        elif frequency == TaskFrequency.WEEKLY:
            return now + timedelta(weeks=1)
        elif frequency == TaskFrequency.MONTHLY:
            return now + timedelta(days=30)

        return now + timedelta(days=1)

    def _create_initial_goals(self, business_id: str, business_type: str):
        """Create initial business goals based on business type"""
        goals = []
        now = datetime.now()

        # Common goals for all businesses
        common_goals = [
            {
                "goal_type": "revenue_growth",
                "target_value": 1000000,  # 1M THB
                "current_value": 0,
                "deadline": now + timedelta(days=365),
                "description": "Achieve 1M THB annual revenue",
            },
            {
                "goal_type": "customer_acquisition",
                "target_value": 100,
                "current_value": 0,
                "deadline": now + timedelta(days=180),
                "description": "Acquire 100 customers",
            },
            {
                "goal_type": "profit_margin",
                "target_value": 20.0,  # 20%
                "current_value": 0,
                "deadline": now + timedelta(days=365),
                "description": "Achieve 20% profit margin",
            },
        ]

        # Business-specific goals
        business_specific_goals = {
            "tech_startup": [
                {
                    "goal_type": "user_growth",
                    "target_value": 1000,
                    "current_value": 0,
                    "deadline": now + timedelta(days=90),
                    "description": "Reach 1000 active users",
                }
            ],
            "restaurant": [
                {
                    "goal_type": "daily_customers",
                    "target_value": 50,
                    "current_value": 0,
                    "deadline": now + timedelta(days=60),
                    "description": "Serve 50 customers daily",
                }
            ],
            "retail_store": [
                {
                    "goal_type": "inventory_turnover",
                    "target_value": 12.0,  # 12 times per year
                    "current_value": 0,
                    "deadline": now + timedelta(days=365),
                    "description": "Achieve 12x inventory turnover",
                }
            ],
        }

        all_goals = common_goals + business_specific_goals.get(business_type, [])

        for goal_data in all_goals:
            goal = BusinessGoal(
                business_id=business_id,
                goal_type=goal_data["goal_type"],
                target_value=goal_data["target_value"],
                current_value=goal_data["current_value"],
                deadline=goal_data["deadline"],
                status="on_track",
                last_updated=now,
            )
            goals.append(goal)

        self.business_goals[business_id] = goals

    async def execute_task(self, task: AutomatedTask):
        """Execute a specific automated task"""
        logger.info(f"Executing task: {task.task_type} for {task.business_name}")

        task.status = TaskStatus.IN_PROGRESS
        task.last_executed = datetime.now()

        try:
            # Send task to appropriate agent
            agent_url = f"http://localhost:{self._get_agent_port(task.agent_type)}"

            message = {
                "agent_type": task.agent_type,
                "task_type": task.task_type,
                "business_id": task.business_id,
                "business_name": task.business_name,
                "parameters": task.parameters or {},
                "timestamp": datetime.now().isoformat(),
                "request_id": f"auto_task_{datetime.now().timestamp()}",
            }

            response = await self.mcp_client.post(
                f"{agent_url}/execute_automated_task",
                json=message,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                result = response.json()
                task.results = result
                task.status = TaskStatus.COMPLETED

                # Update business goals based on task results
                await self._update_goals_from_task(task, result)

                logger.info(f"Task completed successfully: {task.task_type}")
            else:
                task.status = TaskStatus.FAILED
                logger.error(f"Task failed: {task.task_type} - {response.text}")

        except Exception as e:
            task.status = TaskStatus.FAILED
            logger.error(f"Error executing task {task.task_type}: {str(e)}")

        # Schedule next execution
        task.next_execution = self._calculate_next_execution(task.frequency)

    def _get_agent_port(self, agent_type: str) -> int:
        """Get agent port number"""
        ports = {
            "strategic": 5001,
            "creative": 5002,
            "financial": 5003,
            "sales": 5004,
            "manager": 5005,
            "analytics": 5006,
            "swot": 5007,
            "business_model": 5008,
        }
        return ports.get(agent_type, 5001)

    async def _update_goals_from_task(
        self, task: AutomatedTask, result: Dict[str, Any]
    ):
        """Update business goals based on task results"""
        if task.business_id not in self.business_goals:
            return

        goals = self.business_goals[task.business_id]

        # Update goals based on task type and results
        if task.task_type == "kpi_monitoring":
            await self._update_kpi_goals(goals, result)
        elif task.task_type == "financial_review":
            await self._update_financial_goals(goals, result)
        elif task.task_type == "sales_performance":
            await self._update_sales_goals(goals, result)

    async def _update_kpi_goals(
        self, goals: List[BusinessGoal], result: Dict[str, Any]
    ):
        """Update goals based on KPI monitoring results"""
        kpis = result.get("kpis", {})

        for goal in goals:
            if goal.goal_type in kpis:
                goal.current_value = kpis[goal.goal_type]
                goal.last_updated = datetime.now()

                # Update goal status
                progress_percentage = (goal.current_value / goal.target_value) * 100
                time_remaining = (goal.deadline - datetime.now()).days

                if progress_percentage >= 100:
                    goal.status = "achieved"
                elif time_remaining < 30 and progress_percentage < 80:
                    goal.status = "behind"
                elif time_remaining < 60 and progress_percentage < 60:
                    goal.status = "at_risk"
                else:
                    goal.status = "on_track"

    async def _update_financial_goals(
        self, goals: List[BusinessGoal], result: Dict[str, Any]
    ):
        """Update goals based on financial review results"""
        financial_data = result.get("financial_data", {})

        for goal in goals:
            if goal.goal_type == "revenue_growth" and "revenue" in financial_data:
                goal.current_value = financial_data["revenue"]
                goal.last_updated = datetime.now()
            elif (
                goal.goal_type == "profit_margin" and "profit_margin" in financial_data
            ):
                goal.current_value = financial_data["profit_margin"]
                goal.last_updated = datetime.now()

    async def _update_sales_goals(
        self, goals: List[BusinessGoal], result: Dict[str, Any]
    ):
        """Update goals based on sales performance results"""
        sales_data = result.get("sales_data", {})

        for goal in goals:
            if goal.goal_type == "customer_acquisition" and "customers" in sales_data:
                goal.current_value = sales_data["customers"]
                goal.last_updated = datetime.now()

    async def check_goal_achievement(self, business_id: str) -> Dict[str, Any]:
        """Check if business goals are being achieved and trigger re-analysis if needed"""
        if business_id not in self.business_goals:
            return {"needs_reanalysis": False, "reasons": []}

        goals = self.business_goals[business_id]
        reasons = []

        # Check for goals that are behind or at risk
        for goal in goals:
            if goal.status in ["behind", "at_risk"]:
                reasons.append(f"Goal '{goal.goal_type}' is {goal.status}")

        # Check for goals that are significantly behind schedule
        for goal in goals:
            if goal.deadline < datetime.now() and goal.status != "achieved":
                reasons.append(f"Goal '{goal.goal_type}' is past deadline")

        needs_reanalysis = len(reasons) > 0

        if needs_reanalysis:
            logger.warning(f"Business {business_id} needs re-analysis: {reasons}")
            await self._trigger_reanalysis(business_id, reasons)

        return {
            "needs_reanalysis": needs_reanalysis,
            "reasons": reasons,
            "goals_status": {goal.goal_type: goal.status for goal in goals},
        }

    async def _trigger_reanalysis(self, business_id: str, reasons: List[str]):
        """Trigger a new business analysis due to goal underperformance"""
        logger.info(f"Triggering re-analysis for business {business_id}")

        try:
            # Get current business data
            business_data = await self._get_business_data(business_id)
            if not business_data:
                logger.error(f"Could not retrieve business data for {business_id}")
                return

            # Add re-analysis context
            business_data["reanalysis_context"] = {
                "triggered_by": "goal_underperformance",
                "reasons": reasons,
                "original_analysis_date": business_data.get("created_at"),
                "reanalysis_date": datetime.now().isoformat(),
            }

            # Send to main processing endpoint
            response = await self.mcp_client.post(
                "http://localhost:5099/process-business",
                json=business_data,
                headers={"Content-Type": "application/json"},
            )

            if response.status_code == 200:
                logger.info(
                    f"Re-analysis triggered successfully for business {business_id}"
                )
            else:
                logger.error(f"Failed to trigger re-analysis: {response.text}")

        except Exception as e:
            logger.error(f"Error triggering re-analysis: {str(e)}")

    async def _get_business_data(self, business_id: str) -> Optional[Dict[str, Any]]:
        """Get business data from database"""
        try:
            response = await self.mcp_client.get(
                f"http://localhost:5099/get-analysis/{business_id}"
            )
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            logger.error(f"Error getting business data: {str(e)}")
        return None

    async def run_scheduler(self):
        """Main scheduler loop"""
        self.running = True
        logger.info("Starting task automation scheduler")

        while self.running:
            try:
                now = datetime.now()

                # Check for tasks that need to be executed
                for task in self.tasks:
                    if (
                        task.next_execution
                        and task.next_execution <= now
                        and task.status != TaskStatus.IN_PROGRESS
                    ):
                        await self.execute_task(task)

                # Check goal achievement for all businesses
                business_ids = list(self.business_goals.keys())
                for business_id in business_ids:
                    await self.check_goal_achievement(business_id)

                # Wait before next check
                await asyncio.sleep(60)  # Check every minute

            except Exception as e:
                logger.error(f"Error in scheduler loop: {str(e)}")
                await asyncio.sleep(60)

    def stop_scheduler(self):
        """Stop the scheduler"""
        self.running = False
        logger.info("Stopping task automation scheduler")

    def get_business_tasks(self, business_id: str) -> List[AutomatedTask]:
        """Get all tasks for a specific business"""
        return [task for task in self.tasks if task.business_id == business_id]

    def get_business_goals(self, business_id: str) -> List[BusinessGoal]:
        """Get all goals for a specific business"""
        return self.business_goals.get(business_id, [])

    def get_automation_summary(self) -> Dict[str, Any]:
        """Get summary of automation system"""
        return {
            "total_tasks": len(self.tasks),
            "total_businesses": len(self.business_goals),
            "tasks_by_status": {
                status.value: len([t for t in self.tasks if t.status == status])
                for status in TaskStatus
            },
            "recent_activity": [
                {
                    "business_name": task.business_name,
                    "task_type": task.task_type,
                    "status": task.status.value,
                    "last_executed": (
                        task.last_executed.isoformat() if task.last_executed else None
                    ),
                }
                for task in sorted(
                    self.tasks,
                    key=lambda x: x.last_executed or datetime.min,
                    reverse=True,
                )[:10]
            ],
        }


# Global automation engine instance
automation_engine = TaskAutomationEngine()
