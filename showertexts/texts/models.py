import datetime
from django.conf import settings
from django.db import models
from django.utils import timezone


class Subscriber(models.Model):
    sms_number = models.CharField(max_length=20, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    date_renewed = models.DateTimeField()
    lifetime = models.BooleanField(default=False)

    @property
    def expired(self):
        if self.lifetime:
            return False
        # is their renewal date before expiration_days ago?
        return self.date_renewed < timezone.now() - datetime.timedelta(days=settings.EXPIRATION_DAYS)

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
    date = models.DateField(auto_now_add=True)
    post_id = models.CharField(max_length=20)
    thought_text = models.CharField(max_length=500)
    url = models.URLField(max_length=300, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.date) + ' ' + self.thought_text
