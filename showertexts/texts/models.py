from django.db import models

class Subscriber(models.Model):
    sms_number = models.CharField(max_length=20, unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.sms_number

class TextSend(models.Model):
    subscriber = models.ForeignKey(Subscriber)
    date_sent = models.DateTimeField(auto_now_add=True)
    post_id = models.CharField(max_length=20)
    message_text = models.CharField(max_length=500)
