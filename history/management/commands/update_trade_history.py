from django.core.management.base import BaseCommand
from history.services import InstrumentRepository, StockMarketService
import logging

class Command(BaseCommand):
    help = "Updates the trade history for all instruments"

    def handle(self, *args, **kwargs):
        start_message = "Starting trade history update..."
        end_message = "Trade history update completed."

        logging.info(start_message)

        # Refresh instruments and fetch trade history
        InstrumentRepository.refresh_instruments()
        StockMarketService().fetch_and_store_all_trade_history()

        logging.info(end_message)
