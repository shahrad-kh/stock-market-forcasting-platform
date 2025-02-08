from django.core.management.base import BaseCommand
from history.services import InstrumentRepository, StockMarketService

class Command(BaseCommand):
    help = "Updates the trade history for all instruments"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting trade history update...")

        # Refresh instruments and fetch trade history
        InstrumentRepository.refresh_instruments()
        StockMarketService().fetch_and_store_all_trade_history()

        self.stdout.write("Trade history update completed.")
