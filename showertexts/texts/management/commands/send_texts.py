from django.core.management.base import BaseCommand
from util.texter import send_todays_texts


class Command(BaseCommand):
    def handle(self, *args, **options):
        send_todays_texts()
