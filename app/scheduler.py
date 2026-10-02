import logging

from apscheduler.schedulers.background import BackgroundScheduler

from app.jobs.daily_read import run_daily_read


logger = logging.getLogger(__name__)


scheduler = BackgroundScheduler()


def start_scheduler():

    scheduler.add_job(
        run_daily_read,
        trigger="cron",
        hour=8,
        minute=0,
        id="daily-read",
        replace_existing=True,
    )

    scheduler.start()

    logger.info("Daily Read scheduler started.")
