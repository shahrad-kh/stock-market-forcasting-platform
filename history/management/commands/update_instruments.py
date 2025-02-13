from django.core.management.base import BaseCommand
from history.services import InstrumentRepository
import logging

class Command(BaseCommand):
    help = "Refresh instruments"

    def handle(self, *args, **kwargs):
        start_message = "Starting Instruments update..."
        ens_message = "Instruments update completed."
        logging.info(start_message)

        # Refresh instruments
        InstrumentRepository.refresh_instruments()

        logging.info(ens_message)
