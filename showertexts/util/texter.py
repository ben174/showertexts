import praw
from twilio.rest import TwilioRestClient
from custom_settings import ACCOUNT_SID, AUTH_TOKEN, SUBSCRIBERS
from texts import models


client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)

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
    message = "Cool! You'll start receiver Shower Texts daily. " \
        "Reply STOP at any time if you get sick of them. " \
        "Your first one will follow..."
    send_text(subscriber, message, 'initial')
    thought = get_thought()
    print thought
    send_text(subscriber, thought.title, thought.id)

def send_text(subscriber, message, post_id):
    client.messages.create(
        to=subscriber.sms_number,
        from_="+14152002895",
        body=message,
    )
    models.TextSend.objects.create(
        subscriber=subscriber,
        post_id=post_id,
        message_text=message,
    )

def send_todays_texts():
    thought = get_thought()
    for subscriber in Subscriber.objects.filter(active=True):
        print 'Sending text to: ' + str(subscriber)
        send_text(subscriber, thought.title, thought.id)