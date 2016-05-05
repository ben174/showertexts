import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone


class Subscriber(models.Model):
    sms_number = models.CharField(max_length=20, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    date_renewed = models.DateTimeField(null=True, blank=True)
    lifetime = models.BooleanField(default=False)
    note = models.CharField(max_length=100, null=True, blank=True)

    @property
    def expired(self):
        if self.lifetime:
            return False
        date_renewed = self.date_renewed or self.date_created
        # is their renewal date before expiration_days ago?
        return date_renewed < timezone.now() - datetime.timedelta(days=settings.EXPIRATION_DAYS)

    def renew(self):
        self.date_renewed = timezone.now()
        self.active = True

    def __unicode__(self):
        return self.sms_number


class TextSend(models.Model):
    subscriber = models.ForeignKey(Subscriber)
    date_sent = models.DateTimeField(auto_now_add=True)
    post_id = models.CharField(max_length=20)
    message_text = models.CharField(max_length=500)
    result_message = models.CharField(max_length=500, null=True, blank=True)
    sucess = models.BooleanField(default=True)

    def __unicode__(self):
        return self.subscriber.sms_number + ": " + self.post_id + ' - ' + self.message_text


class ShowerThought(models.Model):
    date = models.DateField(null=True, blank=True)
    post_id = models.CharField(max_length=20)
    thought_text = models.CharField(max_length=500)
    url = models.URLField(max_length=300, null=True, blank=True)
    active = models.BooleanField(default=True)
    bot_notified = models.BooleanField(default=False)

    def __unicode__(self):
        return str(self.date) + ' ' + self.thought_text
