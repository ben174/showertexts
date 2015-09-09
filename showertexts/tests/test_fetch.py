import unittest
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
        ret = texter.send_todays_texts()
        assert 'Success' in ret

    def test_expired_subscription(self):
        subscriber = Subscriber.objects.create(sms_number='2096223425')
        subscriber.expired = True
        ret = texter.send_todays_texts()
        print 'exxpired'
        print ret

