from celery.schedules import crontab
from celery.task import periodic_task

@periodic_task(run_every=crontab(hour=0, minute=0))
def scheduled_fetch_and_store_recent_trade_history():
    fetch_and_store_recent_trade_history.delay()