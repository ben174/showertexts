import unittest
import datetime
from django.conf import settings
from django.utils import timezone
from texts.models import ShowerThought, Subscriber
from util import texter
import util.showerthoughts


class TestFetch(unittest.TestCase):
    def test_fetch(self):
        thought = util.showerthoughts.get_todays_thought()
        print thought
        print ShowerThought.objects.all()
        assert ShowerThought.objects.count() == 1


class TestSubscriber(unittest.TestCase):
    def setUp(self):
        Subscriber.objects.all().delete()

    def test_send_all(self):
        subscriber = Subscriber.objects.create(sms_number='2096223425')
        expired_date = timezone.now() - datetime.timedelta(days=settings.EXPIRATION_DAYS+5)
        subscriber.date_created = expired_date
        subscriber.date_renewed = expired_date
        ret = texter.send_todays_expirations()
        assert subscriber.expired
        ret += texter.send_todays_texts()
        print ret
        assert 'Success' in ret

    def test_expired_subscription(self):
        subscriber = Subscriber.objects.create(sms_number='2096223425')
        expired_date = timezone.now() - datetime.timedelta(days=settings.EXPIRATION_DAYS+5)
        subscriber.date_created = expired_date
        subscriber.date_renewed = expired_date
        subscriber.save()
        ret = texter.send_todays_expirations()
        ret += texter.send_todays_texts()

        print 'exxp'
        print ret

