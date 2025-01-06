from django.core.management.base import BaseCommand
from history.services import InstrumentRepository

class Command(BaseCommand):
    help = "Refresh instruments"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Instruments update...")

        # Refresh instruments
        InstrumentRepository.refresh_instruments()

        self.stdout.write("Instruments update completed.")
