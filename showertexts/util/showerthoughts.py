from django.utils import timezone
import praw
from texts.models import ShowerThought


def _validate(submission):
    """
    Validates submission against a set of rules.
    """
    if '/r/' in submission.title:
        return False
    if 'reddit' in submission.title:
        return False
    return True


def get_todays_thought():
    thoughts = ShowerThought.objects.filter(date=timezone.now().date(), active=True)
    if thoughts.exists():
        return thoughts[0]
    new_thought = get_thought()
    return ShowerThought.objects.create(thought_text=new_thought.title,
                                        post_id=new_thought.id,
                                        url=new_thought.url,
                                        date=timezone.now().date())


def get_thought(today=True, rank=1):
    r = praw.Reddit(user_agent='shower_texts')
    params = {}
    if not today:
        params['t'] = 'all'
    submissions = r.get_subreddit('showerthoughts').get_top(limit=rank+10, params=params)
    while True:
        submission = submissions.next()
        if _validate(submission):
            return submission
    return submission


