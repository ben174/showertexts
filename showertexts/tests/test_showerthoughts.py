import unittest
import util.showerthoughts
from texts.models import ShowerThought


class TestFetch(unittest.TestCase):
    def test_fetch(self):
        thought = util.showerthoughts.get_todays_thought()
        print thought
        print ShowerThought.objects.all()
        assert ShowerThought.objects.count() == 1