from django.core.management.base import BaseCommand
from history.services import StockMarketService

class Command(BaseCommand):
    help = "Get the recent trade history for all instruments"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting get recent trade history...")

        # Refresh instruments and fetch trade history
        stock_market_service = StockMarketService()
        stock_market_service.fetch_and_store_recent_trade_history()

        self.stdout.write("Recent trade history update completed.")
