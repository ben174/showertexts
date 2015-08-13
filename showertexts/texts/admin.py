from django.contrib import admin
from texts.models import Subscriber, TextSend, ShowerThought



class TextSendInline(admin.TabularInline):
    exclude = ('hint_log', 'html', 'marks')
    editable = False

    model = TextSend

@admin.register(ShowerThought)
class ShowerThoughtAdmin(admin.ModelAdmin):
    list_display = ('date', 'thought_text', 'post_id', 'active')
    list_filter = ('date', 'active')

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('sms_number', 'date_created', 'active')
    inlines = [
        TextSendInline,
    ]

admin.site.register([TextSend, ])