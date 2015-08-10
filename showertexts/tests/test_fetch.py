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

    def test_send_all(self):
        subscriber = Subscriber.objects.create(sms_number='2096223425')
        ret = texter.send_todays_texts()
        assert ShowerThought.objects.count() == 1
        assert 'Success' in ret
