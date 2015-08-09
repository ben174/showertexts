import os

from django.core.management.base import BaseCommand
from util.texter import send_todays_texts


if 'DJANGO_ADMIN_PASSWORD' in os.environ:
    ACCOUNT_SID = os.environ['TWILIO_SID']
    AUTH_TOKEN = os.environ['TWILIO_TOKEN']
    ADMIN_PASSWORD = os.environ['DJANGO_ADMIN_PASSWORD']

class Command(BaseCommand):
    def handle(self, *args, **options):
        send_todays_texts()
