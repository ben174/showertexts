import logging

from django.conf import settings
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
from texts.models import TextSend, Subscriber
from util.showerthoughts import get_todays_thought


def send_initial_text(subscriber):
    message = "Cool! You'll start receiving Shower Texts daily. " \
        "Reply STOP at any time if you get sick of them. " \
        "Your first one will follow..."
    try:
        send_text(subscriber, message, 'initial')
    except TwilioRestException as e:
        logging.error('Exception sending number to: '  + subscriber.sms_number + ' - ' + str(e))
    thought = get_todays_thought()
    try:
        send_text(subscriber, thought.thought_text, thought.post_id)
    except TwilioRestException as e:
        logging.error('Exception sending number to: '  + subscriber.sms_number + ' - ' + str(e))


def send_text(subscriber, message, post_id):
    client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN)
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
    ret = ""
    thought = get_todays_thought()
    ret += 'Today\'s thought: ' + thought.thought_text + '\n'
    ret += thought.url + '\n'
    for subscriber in Subscriber.objects.filter(active=True):
        ret += 'Sending text to: ' + str(subscriber) + "\n"
        try:
            send_text(subscriber, thought.thought_text, thought.post_id)
            ret += ' - Success\n'
        except DuplicateTextException:
            ret += ' - Duplicate text. Won\'t send.\n'
        except TwilioRestException as ex:
            logging.error('Exception sending number to: '  + subscriber.sms_number + ' - ' + str(ex))
            ret += ' - Exception sending text: ' + str(ex) + '\n'
    return ret

class DuplicateTextException(Exception):
    pass
