from django.core.management.base import BaseCommand
from util.texter import Texter


class Command(BaseCommand):
    def handle(self, *args, **options):
        texter = Texter()
        texter.send_todays_texts()
