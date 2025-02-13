import logging
import pandas as pd
import pytse_client as tse
from pytse_client import symbols_data, Ticker
from history.models import Instrument, History
from datetime import datetime
from django.core.paginator import Paginator
from django.db import connection
from decimal import Decimal, ROUND_HALF_UP
import time


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

class InstrumentRepository:
    @staticmethod
    def refresh_instruments():
        logging.info(f"Start getting symbols...")
        symbols = symbols_data.all_symbols()
        logging.info(f"Getting symbols finished.")

        for symbol in symbols:
            if not Instrument.objects.filter(name=symbol).exists():
                Instrument.objects.create(name=symbol)
                logging.info(f"Instrument data for {symbol} successfully added.")
            else:
                logging.info(f"Instrument data for {symbol} already exists.")
    pass

    @staticmethod
    def get_all_instruments():
        instruments = Instrument.objects.all()
        logging.info(f"Retrieved {len(instruments)} instruments from the database.")
        return instruments

    @staticmethod
    def get_instrument_ids_with_pagination(page_size, page):
        instruments = Instrument.objects.all()
        pagination = Paginator(instruments, page_size)

        if page > pagination.num_pages:
            logging.info(f"Requested page {page} exceeds the total number of pages {pagination.num_pages}. Returning empty list.")
            return []

        page_obj = pagination.get_page(page)
        logging.info(f"Retrieved {len(page_obj)} instruments from the database.")

        return [ins.id for ins in page_obj]
    
    @staticmethod
    def get_instrument_ids_by_name_query_with_pagination(instrument_name_query, page_size, page):
        instruments = Instrument.objects.filter(name__startswith=instrument_name_query).values("id")

        paginator = Paginator(instruments, page_size)

        if page > paginator.num_pages:
            logging.info(f"Requested page {page} exceeds the total number of pages {paginator.num_pages}. Returning empty list.")
            return []

        page_obj = paginator.get_page(page)

        logging.info(f"Retrieved {len(page_obj)} instruments matching '{instrument_name_query}'.")

        return [int(item["id"]) for item in page_obj]


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
    
    @staticmethod
    def get_last_history_for_instruments_by_id(instrument_ids):
            if not instrument_ids:
                return []

            query = """SELECT TOP 2 
                    i.[id] AS InstrumentId,
                    i.[name] AS InstrumentName,
                    h.[id] AS HistoryId,
                    h.[date] AS [Date],
                    h.[close] AS [Close], 
                    h.[open] AS [Open],
                    h.[high] AS [High],
                    h.[low] AS [Low],
                    h.[volume] AS [Volume]
                    FROM history_history AS h
                    INNER JOIN dbo.history_instrument AS i ON h.instrument_id = i.id
                    WHERE h.instrument_id = %s
                    ORDER BY h.id DESC;"""

            logging.info(f"The query generated: {query}")

            query_result = []
            for instrument_id in instrument_ids:
                with connection.cursor() as cursor:
                    cursor.execute(query, [instrument_id])
                    rows = cursor.fetchall()
                    logging.info(f"Fetched rows for instrument {instrument_id}: {rows}")
                    if len(rows) == 0: continue
                    columns = [col[0] for col in cursor.description]

                    ranked_history = [dict(zip(columns, row)) for row in rows]
                    if len(ranked_history) == 2:
                        latest, previous = ranked_history[0], ranked_history[1]
                        if previous["Close"] and previous["Close"] != 0:
                            change = ((Decimal(latest["Close"]) / Decimal(previous["Close"])) - 1) * 100
                            ranked_history[0]["Change"] = float(change.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))
                        else:
                            ranked_history[0]["Change"] = None

                    else:
                        ranked_history[0]["Change"] = None

                    logging.info(f"Processed Data: {ranked_history}")

                    query_result.append(ranked_history[0])
            return query_result  


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

    @staticmethod
    def fetch_and_store_recent_trade_history():
        MAX_RETRIES = 4

        logging.info("Start getting instrument from Db...")
        instruments = InstrumentRepository.get_all_instruments()
        logging.info(f"{len(instruments)} instrument Fetched from Db.")

        for fetched_instrument in instruments:
                symbol_name = fetched_instrument.name
                last_trade_history = HistoryRepository.get_last_history_for_instrument(fetched_instrument)
                logging.info(f"Last trade history for {symbol_name} fetched from Db.")

                if last_trade_history is None:
                    logging.error(f"No trade history available for instrument {symbol_name}")
                    last_trade_date = pd.Timestamp(0)
                else:
                    last_trade_date = pd.Timestamp(last_trade_history.date)

                retry_count = 0
                while retry_count < MAX_RETRIES:
                    try:
                        ticker = Ticker(symbol_name)
                        history = ticker.history

                        if history is None or history.empty:
                            logging.warning(f"No data available for symbol: {symbol_name}")
                            break  # Exit retry loop if no data
                        
                        history['date'] = pd.to_datetime(history.get('date'), errors='coerce')

                        if history['date'].isnull().all():
                            logging.error(f"Invalid date column for {symbol_name}")
                            break
                        
                        recent_trade_data = history[history['date'] > f"{pd.Timestamp(last_trade_date)}"]

                        if recent_trade_data.empty:
                            logging.info(f"No new trade data for {symbol_name}")
                            break
                        
                        logging.info(f"{len(recent_trade_data)} new trade data found for {symbol_name} instrument.")
                        HistoryRepository.save_trade_history_in_bulk(fetched_instrument, recent_trade_data)
                        break  # Success, exit retry loop
                    
                    except Exception as e:
                        retry_count += 1
                        logging.critical(f"Error processing symbol {symbol_name} (Attempt {retry_count}/{MAX_RETRIES}): {e}")
                        if retry_count < MAX_RETRIES:
                            time.sleep(2 ** retry_count)  # Exponential backoff before retrying
                        else:
                            logging.error(f"Max retries reached for {symbol_name}. Skipping to next instrument.")
                            break
                        
