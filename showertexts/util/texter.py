from django.conf import settings
import praw
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
from texts.models import TextSend, Subscriber
import logging

client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

def get_thought(today=True, rank=1):
    r = praw.Reddit(user_agent='shower_texts')
    params = {}
    if not today:
        params['t'] = 'all'
    submissions = r.get_subreddit('showerthoughts').get_top(limit=rank, params=params)
    for _ in range(rank):
        submission = submissions.next()
    return submission

def send_initial_text(subscriber):
    message = "Cool! You'll start receiving Shower Texts daily. " \
        "Reply STOP at any time if you get sick of them. " \
        "Your first one will follow..."
    try:
        send_text(subscriber, message, 'initial')
    except TwilioRestException as e:
        logging.error('Exception sending number to: '  + subscriber.sms_number + ' - ' + str(e))
    thought = get_thought()
    try:
        send_text(subscriber, thought.title, thought.id)
    except TwilioRestException as e:
        logging.error('Exception sending number to: '  + subscriber.sms_number + ' - ' + str(e))

def send_text(subscriber, message, post_id):
    if TextSend.objects.filter(subscriber=subscriber, post_id=post_id).exists():
        logging.warning('Attempted to send a duplicate text. Won\'t do it.')
        raise DuplicateTextException()
    client.messages.create(
        to=subscriber.sms_number,
        from_="+14152002895",
        body=message,
    )
    TextSend.objects.create(
        subscriber=subscriber,
        post_id=post_id,
        message_text=message,
    )

def send_todays_texts():
    thought = get_thought()
    for subscriber in Subscriber.objects.filter(active=True):
        logging.info('Sending text to: ' + str(subscriber))
        send_text(subscriber, thought.title, thought.id)

class DuplicateTextException(Exception):
    pass
