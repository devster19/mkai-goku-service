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

# Import database module for persistent storage
from database import BusinessDatabase

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
    task_id: Optional[str] = None  # Database ID for the task


@dataclass
class BusinessGoal:
    business_id: str
    goal_type: str
    target_value: float
    current_value: float
    deadline: datetime
    status: str  # "on_track", "at_risk", "behind", "achieved"
    last_updated: datetime
    goal_id: Optional[str] = None  # Database ID for the goal


class TaskAutomationEngine:
    """Automated task management and business monitoring system"""

    def __init__(self):
        self.db = BusinessDatabase()
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

                # Create task data for database
                task_data = {
                    "business_id": business_id,
                    "business_name": business_name,
                    "agent_type": agent_type,
                    "task_type": task_type,
                    "frequency": frequency.value,
                    "next_execution": self._calculate_next_execution(frequency),
                    "parameters": task_config["parameters"],
                    "status": TaskStatus.PENDING.value,
                }

                # Save task to database
                task_id = self.db.save_task(task_data)
                if task_id:
                    logger.info(f"✅ Created task {task_type} for {business_name}")

        # Create initial business goals
        self._create_initial_goals(business_id, business_type)

        logger.info(f"Created automation tasks for {business_name}")

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
        else:
            return now + timedelta(days=1)

    def _create_initial_goals(self, business_id: str, business_type: str):
        """Create initial business goals based on business type"""
        goals = []

        # Common goals for all business types
        common_goals = [
            {
                "goal_type": "revenue_growth",
                "target_value": 1000000,  # 1M THB
                "current_value": 0,
                "deadline": datetime.now() + timedelta(days=365),
                "status": "on_track",
            },
            {
                "goal_type": "customer_acquisition",
                "target_value": 1000,
                "current_value": 0,
                "deadline": datetime.now() + timedelta(days=180),
                "status": "on_track",
            },
        ]

        # Business-specific goals
        business_specific_goals = {
            "tech_startup": [
                {
                    "goal_type": "user_engagement",
                    "target_value": 80,  # 80% engagement rate
                    "current_value": 0,
                    "deadline": datetime.now() + timedelta(days=90),
                    "status": "on_track",
                },
            ],
            "restaurant": [
                {
                    "goal_type": "daily_customers",
                    "target_value": 200,
                    "current_value": 0,
                    "deadline": datetime.now() + timedelta(days=60),
                    "status": "on_track",
                },
            ],
            "retail_store": [
                {
                    "goal_type": "inventory_turnover",
                    "target_value": 12,  # 12 times per year
                    "current_value": 0,
                    "deadline": datetime.now() + timedelta(days=90),
                    "status": "on_track",
                },
            ],
        }

        # Combine common and business-specific goals
        all_goals = common_goals + business_specific_goals.get(business_type, [])

        # Save goals to database
        for goal_data in all_goals:
            goal_data["business_id"] = business_id
            goal_id = self.db.save_goal(goal_data)
            if goal_id:
                logger.info(
                    f"✅ Created goal {goal_data['goal_type']} for business {business_id}"
                )

    async def execute_task(self, task: AutomatedTask):
        """Execute a specific automated task"""
        try:
            # Update task status to in_progress
            if task.task_id:
                self.db.update_task(
                    task.task_id, {"status": TaskStatus.IN_PROGRESS.value}
                )

            logger.info(
                f"🤖 {task.agent_type.title()} Agent - Automated Task Received:"
            )
            logger.info(f"   Task Type: {task.task_type}")
            logger.info(f"   Business: {task.business_name}")
            logger.info(f"   Business ID: {task.business_id}")
            logger.info(f"   Parameters: {task.parameters}")

            # Get agent port
            agent_port = self._get_agent_port(task.agent_type)
            agent_url = f"http://localhost:{agent_port}"

            # Execute task via agent
            task_request = {
                "task_type": task.task_type,
                "business_id": task.business_id,
                "business_name": task.business_name,
                "parameters": task.parameters or {},
            }

            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{agent_url}/execute_automated_task",
                    json=task_request,
                )

                if response.status_code == 200:
                    result = response.json()

                    # Update task with results
                    update_data = {
                        "status": TaskStatus.COMPLETED.value,
                        "results": result,
                        "last_executed": datetime.now(),
                        "next_execution": self._calculate_next_execution(
                            task.frequency
                        ),
                    }

                    if task.task_id:
                        self.db.update_task(task.task_id, update_data)

                    # Update goals based on task results
                    await self._update_goals_from_task(task, result)

                    logger.info(
                        f"✅ {task.agent_type.title()} Agent - Task Completed: {task.task_type}"
                    )
                else:
                    # Update task status to failed
                    if task.task_id:
                        self.db.update_task(
                            task.task_id,
                            {
                                "status": TaskStatus.FAILED.value,
                                "last_executed": datetime.now(),
                            },
                        )
                    logger.error(f"❌ Task execution failed: {response.status_code}")

        except Exception as e:
            logger.error(f"❌ Error executing task: {e}")
            # Update task status to failed
            if task.task_id:
                self.db.update_task(
                    task.task_id,
                    {
                        "status": TaskStatus.FAILED.value,
                        "last_executed": datetime.now(),
                    },
                )

    def _get_agent_port(self, agent_type: str) -> int:
        """Get the port number for a specific agent type"""
        agent_ports = {
            "strategic": 5001,
            "creative": 5002,
            "financial": 5003,
            "sales": 5004,
            "manager": 5005,
            "analytics": 5006,
            "swot": 5007,
            "business_model": 5008,
        }
        return agent_ports.get(agent_type, 5001)

    async def _update_goals_from_task(
        self, task: AutomatedTask, result: Dict[str, Any]
    ):
        """Update business goals based on task results"""
        try:
            # Get current goals for the business
            goals_data = self.db.get_goals_for_business(task.business_id)

            if not goals_data:
                return

            # Update goals based on task type and results
            if task.task_type == "financial_review":
                await self._update_financial_goals(goals_data, result)
            elif task.task_type == "sales_performance":
                await self._update_sales_goals(goals_data, result)
            elif task.task_type == "kpi_monitoring":
                await self._update_kpi_goals(goals_data, result)

        except Exception as e:
            logger.error(f"❌ Error updating goals from task: {e}")

    async def _update_kpi_goals(
        self, goals: List[Dict[str, Any]], result: Dict[str, Any]
    ):
        """Update KPI-related goals"""
        for goal in goals:
            if goal["goal_type"] == "user_engagement":
                # Update based on engagement metrics
                if "engagement_rate" in result:
                    self.db.update_goal(
                        goal["_id"], {"current_value": result["engagement_rate"]}
                    )

    async def _update_financial_goals(
        self, goals: List[Dict[str, Any]], result: Dict[str, Any]
    ):
        """Update financial goals"""
        for goal in goals:
            if goal["goal_type"] == "revenue_growth":
                # Update based on financial metrics
                if "current_revenue" in result:
                    self.db.update_goal(
                        goal["_id"], {"current_value": result["current_revenue"]}
                    )

    async def _update_sales_goals(
        self, goals: List[Dict[str, Any]], result: Dict[str, Any]
    ):
        """Update sales goals"""
        for goal in goals:
            if goal["goal_type"] == "customer_acquisition":
                # Update based on sales metrics
                if "total_customers" in result:
                    self.db.update_goal(
                        goal["_id"], {"current_value": result["total_customers"]}
                    )

    async def check_goal_achievement(self, business_id: str) -> Dict[str, Any]:
        """Check if business goals are being achieved and trigger re-analysis if needed"""
        try:
            goals_data = self.db.get_goals_for_business(business_id)

            if not goals_data:
                return {"message": "No goals found for this business"}

            at_risk_goals = []
            behind_goals = []
            achieved_goals = []

            for goal in goals_data:
                progress = (
                    (goal["current_value"] / goal["target_value"]) * 100
                    if goal["target_value"] > 0
                    else 0
                )
                days_remaining = (
                    datetime.fromisoformat(goal["deadline"]) - datetime.now()
                ).days

                # Update goal status based on progress and time remaining
                if progress >= 100:
                    status = "achieved"
                    achieved_goals.append(goal["goal_type"])
                elif days_remaining < 30 and progress < 70:
                    status = "at_risk"
                    at_risk_goals.append(goal["goal_type"])
                elif days_remaining < 60 and progress < 50:
                    status = "behind"
                    behind_goals.append(goal["goal_type"])
                else:
                    status = "on_track"

                # Update goal status in database
                self.db.update_goal(goal["_id"], {"status": status})

            # Trigger re-analysis if goals are at risk
            if at_risk_goals or behind_goals:
                await self._trigger_reanalysis(
                    business_id, at_risk_goals + behind_goals
                )

            return {
                "business_id": business_id,
                "goals_status": {
                    "achieved": achieved_goals,
                    "at_risk": at_risk_goals,
                    "behind": behind_goals,
                    "on_track": [
                        g["goal_type"] for g in goals_data if g["status"] == "on_track"
                    ],
                },
                "total_goals": len(goals_data),
                "achievement_rate": (
                    len(achieved_goals) / len(goals_data) * 100 if goals_data else 0
                ),
            }

        except Exception as e:
            logger.error(f"❌ Error checking goal achievement: {e}")
            return {"error": str(e)}

    async def _trigger_reanalysis(self, business_id: str, reasons: List[str]):
        """Trigger re-analysis of business due to goal issues"""
        try:
            logger.warning(
                f"⚠️ Triggering re-analysis for business {business_id} due to: {reasons}"
            )

            # Get business data
            business_data = await self._get_business_data(business_id)
            if not business_data:
                return

            # Create re-analysis task
            reanalysis_task = {
                "business_id": business_id,
                "business_name": business_data.get("business_name", "Unknown"),
                "agent_type": "manager",
                "task_type": "goal_review",
                "frequency": TaskFrequency.MONTHLY.value,
                "parameters": {"review_type": "goal_crisis", "reasons": reasons},
                "status": TaskStatus.PENDING.value,
                "next_execution": datetime.now(),
            }

            # Save re-analysis task
            task_id = self.db.save_task(reanalysis_task)
            if task_id:
                logger.info(f"✅ Created re-analysis task for business {business_id}")

        except Exception as e:
            logger.error(f"❌ Error triggering re-analysis: {e}")

    async def _get_business_data(self, business_id: str) -> Optional[Dict[str, Any]]:
        """Get business data from database"""
        try:
            return self.db.get_business(business_id)
        except Exception as e:
            logger.error(f"❌ Error getting business data: {e}")
            return None

    async def run_scheduler(self):
        """Run the task scheduler"""
        self.running = True
        logger.info("🚀 Starting automation scheduler...")

        while self.running:
            try:
                # Get all pending tasks that are due for execution
                now = datetime.now()
                all_tasks = self.db.get_all_tasks()

                for task_data in all_tasks:
                    if task_data["status"] == TaskStatus.PENDING.value:
                        next_execution = datetime.fromisoformat(
                            task_data["next_execution"]
                        )
                        if next_execution <= now:
                            # Create AutomatedTask object
                            task = AutomatedTask(
                                business_id=task_data["business_id"],
                                business_name=task_data["business_name"],
                                agent_type=task_data["agent_type"],
                                task_type=task_data["task_type"],
                                frequency=TaskFrequency(task_data["frequency"]),
                                parameters=task_data.get("parameters", {}),
                                task_id=task_data["_id"],
                            )

                            # Execute task
                            await self.execute_task(task)

                # Sleep for 1 minute before next check
                await asyncio.sleep(60)

            except Exception as e:
                logger.error(f"❌ Scheduler error: {e}")
                await asyncio.sleep(60)

    def stop_scheduler(self):
        """Stop the task scheduler"""
        self.running = False
        logger.info("🛑 Stopping automation scheduler...")

    def get_business_tasks(self, business_id: str) -> List[Dict[str, Any]]:
        """Get all tasks for a specific business"""
        return self.db.get_tasks_for_business(business_id)

    def get_business_goals(self, business_id: str) -> List[Dict[str, Any]]:
        """Get all goals for a specific business"""
        return self.db.get_goals_for_business(business_id)

    def get_automation_summary(self) -> Dict[str, Any]:
        """Get automation system summary"""
        try:
            all_tasks = self.db.get_all_tasks()

            # Calculate statistics
            total_tasks = len(all_tasks)
            pending_tasks = len(
                [t for t in all_tasks if t["status"] == TaskStatus.PENDING.value]
            )
            completed_tasks = len(
                [t for t in all_tasks if t["status"] == TaskStatus.COMPLETED.value]
            )
            failed_tasks = len(
                [t for t in all_tasks if t["status"] == TaskStatus.FAILED.value]
            )

            # Group by business
            business_tasks = {}
            for task in all_tasks:
                business_id = task["business_id"]
                if business_id not in business_tasks:
                    business_tasks[business_id] = []
                business_tasks[business_id].append(task)

            return {
                "total_tasks": total_tasks,
                "pending_tasks": pending_tasks,
                "completed_tasks": completed_tasks,
                "failed_tasks": failed_tasks,
                "success_rate": (
                    (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
                ),
                "businesses_with_tasks": len(business_tasks),
                "scheduler_status": "running" if self.running else "stopped",
                "last_updated": datetime.now().isoformat(),
            }

        except Exception as e:
            logger.error(f"❌ Error getting automation summary: {e}")
            return {"error": str(e)}


# Global automation engine instance
automation_engine = TaskAutomationEngine()
