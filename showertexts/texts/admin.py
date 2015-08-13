from django.contrib import admin
from texts.models import Subscriber, TextSend, ShowerThought


class TextSendInline(admin.TabularInline):
    editable = False
    model = TextSend


@admin.register(ShowerThought)
class ShowerThoughtAdmin(admin.ModelAdmin):
    list_display = ('date', 'thought_text', 'post_id', 'active', )
    list_filter = ('date', 'active', )


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('sms_number', 'date_created', 'active', )
    inlines = [
        TextSendInline,
    ]
    search_fields = ('sms_number', )
    list_filter = ('active', )


@admin.register(TextSend)
class TextSendAdmin(admin.ModelAdmin):
    list_display = ('date_sent', 'subscriber', 'message_text', 'sucess', 'result_message', )
    list_filter = ('date_sent', 'sucess', )
