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

    def __unicode__(self):
        return self.subscriber.sms_number + ": " + self.post_id + ' - ' + self.message_text

class ShowerThought(models.Model):
    date = models.DateField(auto_now_add=True)
    post_id = models.CharField(max_length=20)
    thought_text = models.CharField(max_length=500)
    url = models.URLField(max_length=100)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.date) + ' ' + self.thought_text
