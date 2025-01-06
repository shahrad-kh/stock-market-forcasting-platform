import logging
import pandas as pd
import pytse_client as tse
from pytse_client import symbols_data
from history.models import Instrument, History, RecentUpdate
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class InstrumentRepository:
    @staticmethod
    def refresh_instruments():
        symbols = symbols_data.all_symbols()

        for symbol in symbols:
            if not Instrument.objects.filter(name=symbol).exists():
                Instrument.objects.create(name=symbol)
                logging.info(f"Instrument data for {symbol} successfully added.")

    @staticmethod
    def get_all_instruments():
        instruments = Instrument.objects.all()
        logging.info(f"Retrieved {len(instruments)} instruments from the database.")
        return instruments

class HistoryRepository:
    @staticmethod
    def clear_history_for_instrument(instrument):
        History.objects.filter(instrument=instrument).delete()
        logging.info(f"Cleared history for instrument: {instrument.name}.")

    @staticmethod
    def save_trade_history(instrument, trade_data):
        for _, row in trade_data.iterrows():
            History.objects.create(
                instrument=instrument,
                date=row['date'],
                open=row['open'],
                high=row['high'],
                low=row['low'],
                close=row['close'],
            )
        logging.info(f"Saved trade history for instrument: {instrument.name}.")

class RecentUpdateRepository:
    @staticmethod
    def add_record():
        RecentUpdate.objects.create(recent_update_date_time = datetime.now())
        logging.info("New recent update record added")


class StockMarketService:
    def fetch_and_store_all_trade_history(self):
        instruments = InstrumentRepository.get_all_instruments()

        for fetched_instrument in instruments:
            symbol = fetched_instrument.name
            HistoryRepository.clear_history_for_instrument(fetched_instrument)

            try:
                history = tse.download(symbol, write_to_csv=False)
                if not history:
                    logging.warning(f"No data available for symbol: {symbol}")
                    continue

                trade_data = pd.DataFrame(history[symbol])
                HistoryRepository.save_trade_history(fetched_instrument, trade_data)

            except Exception as e:
                logging.error(f"Error processing symbol {symbol}: {e}")
        
        
