import logging
from celery.schedules import crontab
from celery import shared_task
from history.services import StockMarketService

@shared_task
def scheduled_fetch_and_store_recent_trade_history():
    logging.info("scheduled_fetch_and_store_recent_trade_history task have been executed.")
    StockMarketService.fetch_and_store_recent_trade_history()    