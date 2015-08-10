from django.contrib import admin
from texts.models import Subscriber, TextSend, ShowerThought

admin.site.register([Subscriber, TextSend, ShowerThought])
