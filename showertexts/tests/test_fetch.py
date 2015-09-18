import unittest
import datetime
from django.conf import settings
from django.utils import timezone
from texts.models import ShowerThought, Subscriber, TextSend
from texts.views import subscribe_number
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
        subscriber.save()
        ret = texter.send_todays_texts()
        assert ret[0]['action'] == 'showertext'
        assert TextSend.objects.count() == 1

    def test_expired_subscription(self):
        subscriber = Subscriber.objects.create(sms_number='2096223425')
        expired_date = timezone.now() - datetime.timedelta(days=settings.EXPIRATION_DAYS + 5)
        subscriber.date_created = expired_date
        subscriber.date_renewed = expired_date
        subscriber.save()
        ret = texter.send_todays_texts()

        assert subscriber.expired
        assert ret[0]['action'] == 'expiration'
        assert len(ret) == 1
        assert TextSend.objects.count() == 1

        welcome_message = subscribe_number('2096223425')
        assert 'Welcome back!' in welcome_message

        subscriber = Subscriber.objects.get(sms_number='2096223425')
        assert not subscriber.expired
        assert TextSend.objects.count() == 2
