import unittest
import util.showerthoughts
from texts.models import ShowerThought


class TestFetch(unittest.TestCase):
    def test_fetch(self):
        thought = util.showerthoughts.get_todays_thought()
        print thought
        print ShowerThought.objects.all()
        assert ShowerThought.objects.count() == 1

    def test_no_duplicate(self):
        todays_thought = util.showerthoughts.get_todays_thought()
        submission = util.showerthoughts.get_thought()
        self.assertNotEqual(todays_thought.post_id, submission.id)



