import datetime
from django.utils import timezone
import praw
from texts.models import ShowerThought

banned_phrases = [
    '/r/',
    'reddit',
    'dick',
    'blow job',
]

def _validate(submission):
    """
    Validates submission against a set of rules.
    """
    title = submission.title.lower()
    return not any([bad_word in title for bad_word in banned_phrases])


def get_todays_thought():
    thoughts = ShowerThought.objects.filter(date=datetime.datetime.today(), active=True)
    if thoughts.exists():
        return thoughts[0]
    new_thought = get_thought()
    return ShowerThought.objects.create(thought_text=new_thought.title,
                                        post_id=new_thought.id,
                                        url=new_thought.url,
                                        date=datetime.datetime.today())


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


