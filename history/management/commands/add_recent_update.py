from django.core.management.base import BaseCommand
from history.services import RecentUpdateRepository

class Command(BaseCommand):
    help = "Add Recent Update Record"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting Adding Recent update Record...")

        # add record
        RecentUpdateRepository.add_record()

        self.stdout.write("Recent update Record Added.")
