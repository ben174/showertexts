import datetime
from django.core.cache import cache
import praw
from showertexts import settings
from texts.models import ShowerThought
from util.showerbot import ShowerBot

banned_phrases = [
    '/r/',
    'reddit',
    'dick',
    'blow job',
    'r/',
    'gonewild',
]

#TODO: Exclude posts which have a body

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
    showerthought = ShowerThought.objects.create(thought_text=new_thought.title,
                                                 post_id=new_thought.id,
                                                 url=new_thought.url,
                                                 date=datetime.datetime.today())
    cache.set('todays_thought_text', new_thought.title)
    # post a notification comment on the thread for this showerthought
    bot = ShowerBot()
    bot.login()
    bot.post_notification(showerthought)
    return showerthought


def random_thought():
    return ShowerThought.objects.order_by('?').first()


def choose_alternate(submission_id):
    r = praw.Reddit(user_agent=settings.REDDIT_USER_AGENT)
    submission = r.get_submission(submission_id=submission_id)
    showerthought, _ = ShowerThought.objects.get_or_create(date=datetime.datetime.today())
    showerthought.thought_text = submission.title
    showerthought.post_id = submission.id
    showerthought.url = submission.url
    showerthought.save()
    cache.set('todays_thought_text', showerthought.thought_text)


def get_thought(today=True, rank=1):
    r = praw.Reddit(user_agent=settings.REDDIT_USER_AGENT)
    params = {}
    if not today:
        params['t'] = 'all'
    submissions = r.get_subreddit('showerthoughts').get_top(limit=rank + 10, params=params)
    while True:
        submission = submissions.next()
        if _validate(submission):
            return submission
    return submission


def get_submissions():
    r = praw.Reddit(user_agent=settings.REDDIT_USER_AGENT)
    submissions = r.get_subreddit('showerthoughts').get_top(limit=10)
    while True:
        submission = submissions.next()
        if _validate(submission):
            yield submission