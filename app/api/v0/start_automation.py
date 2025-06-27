#!/usr/bin/env python3
"""
Start the automation system for business monitoring and task execution
"""

import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from task_automation import automation_engine
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    """Main function to start the automation system"""
    try:
        logger.info("🚀 Starting Business Automation System...")
        logger.info(
            "📊 This system will monitor business goals and execute automated tasks"
        )
        logger.info(
            "⏰ Tasks will run based on their configured frequency (daily, weekly, monthly)"
        )
        logger.info("🎯 Goals will be checked and re-analysis triggered if needed")
        logger.info("")
        logger.info("Press Ctrl+C to stop the automation system")
        logger.info("=" * 60)

        # Start the automation scheduler
        await automation_engine.run_scheduler()

    except KeyboardInterrupt:
        logger.info("")
        logger.info("🛑 Stopping automation system...")
        automation_engine.stop_scheduler()
        logger.info("✅ Automation system stopped successfully")
    except Exception as e:
        logger.error(f"❌ Error in automation system: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
