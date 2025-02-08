import logging
import pandas as pd
import pytse_client as tse
from celery import shared_task
from pytse_client import symbols_data, Ticker
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
                volume=row['volume']
            )
        logging.info(f"Saved trade history for instrument: {instrument.name}.")

    @staticmethod
    def save_trade_history_in_bulk(instrument, trade_data):
        bulk_records = []
        
        for _, row in trade_data.iterrows():
            bulk_records.append(
                History(
                    instrument=instrument,
                    date=row['date'],
                    open=row['open'],
                    high=row['high'],
                    low=row['low'],
                    close=row['close'],
                    volume=row['volume']
                )
            )
        if bulk_records:
            History.objects.bulk_create(bulk_records, batch_size=500)
            logging.info(f"Saved {len(bulk_records)} trade history records in bulk.")
        else:
            logging.info("No new trade history records to save.")

    @staticmethod
    def get_last_history_for_instrument(instrument):
        return History.objects.all().filter(instrument=instrument).order_by("-date").first()

        
class RecentUpdateRepository:
    @staticmethod
    def add_record():
        RecentUpdate.objects.create(recent_update_date_time = datetime.now())
        logging.info("New recent update record added")

    def get_recent_update_record():
        RecentUpdate.objects.all().order_by("-recent_update_date_time").first()
        logging.info("Recent update record fetch from database")



class StockMarketService:
    @staticmethod
    def fetch_and_store_all_trade_history():
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

    @shared_task
    def fetch_and_store_recent_trade_history():
        instruments = InstrumentRepository.get_all_instruments()

        for fetched_instrument in instruments:
            symbol_name = fetched_instrument.name
            last_trade_history = HistoryRepository.get_last_history_for_instrument(fetched_instrument)
           
            if last_trade_history is None:
                logging.error(f"No trade history avaiable for instrumrnt {symbol_name}")
                continue
            
            last_trade_date = pd.Timestamp(last_trade_history.date)

            try:
                ticker = Ticker(symbol_name)
                history = ticker.history

                if history is None or history.empty:
                    logging.warning(f"No data available for symbol: {symbol_name}")
                    continue

                history['date'] = pd.to_datetime(history.get('date'), errors='coerce')

                if history['date'].isnull().all():
                    logging.error(f"Invalid date column for {symbol_name}")
                    continue
                
                recent_trade_data = history[history['date'] > f"{pd.Timestamp(last_trade_date)}"]
                
                if recent_trade_data.empty:
                    logging.info(f"No new trade data for {symbol_name}")
                    continue

                HistoryRepository.save_trade_history(fetched_instrument, recent_trade_data)

            except Exception as e:
                logging.error(f"Error processing symbol {symbol_name}: {e}")

        
