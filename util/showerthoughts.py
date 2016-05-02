import datetime
import logging
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


def _validate(submission):
    """
    Validates submission against a set of rules.
    """
    title = submission.title.lower()
    if ShowerThought.objects.filter(post_id=submission.id).exists():
        # sometimes posts are chosen for two days because they fall right on the cusp
        logging.warning("Post has already been used: " + submission.title)
        return False
    return not any([bad_word in title for bad_word in banned_phrases])


def get_todays_thought():
    # first try to get a thought assigned to today
    thought = ShowerThought.objects.filter(date=datetime.datetime.today(), active=True).first()
    if thought:
        return thought

    # otherwise try to get an unused thought that's not assigned to any date
    thought = ShowerThought.objects.filter(date__isnull=True, active=True).first()
    if thought:
        thought.date = datetime.datetime.today()
        thought.save()
        return thought

    # last resort grab whatever today's top shower thought is
    new_thought = get_thought()
    showerthought = ShowerThought.objects.create(thought_text=new_thought.title,
                                                 post_id=new_thought.id,
                                                 url=new_thought.url,
                                                 date=datetime.datetime.today(),
                                                 active=True)
    cache.set('todays_thought_text', new_thought.title)
    # post a notification comment on the thread for this showerthought
    bot = ShowerBot()
    bot.login()
    bot.post_notification(showerthought)
    return showerthought


def random_thought():
    return ShowerThought.objects.filter(active=True).order_by('?').first()


def choose_alternate(submission_id):
    """
    Invalidates the currently chosen thought and
    """
    r = praw.Reddit(user_agent=settings.REDDIT_USER_AGENT)
    submission = r.get_submission(submission_id=submission_id)
    # set any other posts selected for today as inactive
    ShowerThought.objects.filter(date=datetime.datetime.today()).update(active=False)
    showerthought, created = ShowerThought.objects.get_or_create(
        date=datetime.datetime.today(),
        post_id=submission.id,
        thought_text=submission.title,
        url=submission.url
    )
    if not created:
        # i guess i changed my mind, revive this old one
        showerthought.active = True
        showerthought.save()
    cache.set('todays_thought_text', showerthought.thought_text)


def queue_alternate(submission_id):
    """
    Queues up an alternative post for a rainy day
    """
    r = praw.Reddit(user_agent=settings.REDDIT_USER_AGENT)
    submission = r.get_submission(submission_id=submission_id)
    # set any other posts selected for today as inactive
    showerthought, created = ShowerThought.objects.get_or_create(
        post_id=submission.id,
        thought_text=submission.title,
        url=submission.url
    )
    if not created:
        # i guess i changed my mind, revive this old one
        showerthought.active = True
        showerthought.save()


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
