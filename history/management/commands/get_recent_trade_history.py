from django.core.management.base import BaseCommand
from history.services import StockMarketService
import logging


class Command(BaseCommand):
    help = "Get the recent trade history for all instruments"

    def handle(self, *args, **kwargs):
        start_message = "Starting get recent trade history..."
        end_message = "Recent trade history update completed."
        logging.info(start_message)

        # Refresh instruments and fetch trade history
        StockMarketService.fetch_and_store_recent_trade_history()

        logging.info(end_message)
        pass
