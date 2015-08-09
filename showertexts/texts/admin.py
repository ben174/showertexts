from django.contrib import admin
from texts.models import Subscriber, TextSend

admin.site.register([Subscriber, TextSend])
