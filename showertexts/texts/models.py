from django.db import models

class Subscriber(models.Model):
    user = models.OneToOneField(User)
    sms_number = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
