import logging
import praw
from showertexts import settings


class ShowerBot(object):
    """ A bot which automatically notifies the /r/showerthoughts submission which was chosen for today's shower thought.

    """

    def __init__(self):
        self.reddit = praw.Reddit(user_agent=settings.REDDIT_USER_AGENT)

    def login(self):
        self.reddit.login(settings.REDDIT_USERNAME, settings.REDDIT_PASSWORD)

    def post_notification(self, thought):
        if thought.bot_notified:
            logging.warning('Notification already posted to reddit.')
            return
        try:
            if settings.ENABLE_SHOWERBOT:
                submission = self.reddit.get_submission(submission_id=thought.post_id)
                submission.add_comment('Cool! This post has been selected as today\'s '
                                       '[ShowerText](http://www.showertexts.com). ShowerTexts is a completely free '
                                       'service which automatically sends you today\'s top /r/showerthoughts to your '
                                       'phone.\n\n'
                                       'http://www.showertexts.com\n\n'
                                       '_____________________________________________\n\n'
                                       '*^This ^message ^was ^automatically ^posted ^by '
                                       '^[showerbot](https://github.com/ben174/showertexts/blob/master/util/showerbot.py) '
                                       '^If ^I ^misbehave ^or ^otherwise ^become ^annoying, ^please ^notify ^my ^owner, '
                                       '^/u/ben174. [^View ^the ^source ^code ^here.](https://github.com/ben174/showertexts/)*')
            else:
                logging.info("Pretending to submit to reddit.")
            thought.bot_notified = True
            thought.save()
        except Exception as ex:
            logging.error('Exception while posting reddit bot notification. ' + ex.message)
            logging.error(str(ex))
