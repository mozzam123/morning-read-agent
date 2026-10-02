import logging

from apscheduler.schedulers.background import BackgroundScheduler

from app.core.config import settings
from app.jobs.daily_read import run_daily_read


logger = logging.getLogger(__name__)


scheduler = BackgroundScheduler(timezone=settings.scheduler_timezone)


def start_scheduler():

    scheduler.add_job(
        run_daily_read,
        trigger="cron",
        hour=settings.daily_read_hour,
        minute=settings.daily_read_minute,
        id="daily-read",
        replace_existing=True,
    )

    scheduler.start()

    logger.info(
        "Daily Read scheduler started: %02d:%02d (%s)",
        settings.daily_read_hour,
        settings.daily_read_minute,
        settings.scheduler_timezone,
    )
