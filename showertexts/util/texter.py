import logging
import datetime

from django.conf import settings
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
from texts.models import TextSend, Subscriber
from util.showerthoughts import get_todays_thought


def send_text(subscriber, message, post_id):
    client = TwilioRestClient(settings.ACCOUNT_SID, settings.AUTH_TOKEN)

    if TextSend.objects.filter(subscriber=subscriber, post_id=post_id).exists():
        logging.warning('Attempted to send a duplicate text. Won\'t do it.')
        raise DuplicateTextException()
    try:
        client.messages.create(
            to=subscriber.sms_number,
            from_=settings.TWILIO_NUMBER,
            body=message,
        )
    except TwilioRestException as e:
        logging.error('Exception sending number to: '  + subscriber.sms_number + ' - ' + str(e))
        TextSend.objects.create(
            subscriber=subscriber,
            post_id=post_id,
            message_text=message,
            sucess=False,
            result_message=str(e),
        )
        #TODO: refactor into a configurable list
        if 'not a valid phone number' in str(e) or 'violates a blacklist rule' in str(e) or 'not a mobile number' in str(e):
            subscriber.active = False
            subscriber.save()
        raise e
    TextSend.objects.create(
        subscriber=subscriber,
        post_id=post_id,
        message_text=message,
    )


def send_todays_expirations():
    ret = []
    expiry_date = datetime.datetime.now() - datetime.timedelta(days=settings.EXPIRATION_DAYS)
    expiring_subscribers = Subscriber.objects.filter(active=True, date_renewed__lte=expiry_date)
    notice = 'HOUSE KEEPING! I\'m clearing out old numbers to make room for more. If you like these, please ' \
             'resubscribe for free! http://www.showertexts.com'
    post_id = 'EXP-' + str(datetime.date.today())
    for subscriber in expiring_subscribers:
        row = {'to': subscriber, 'action': 'expiration'}
        try:
            send_text(subscriber, notice, post_id)
            row['result'] = 'Success'
        except DuplicateTextException:
            row['result'] = 'Duplicate'
        except TwilioRestException as ex:
            row['result'] = 'Exception: ' + str(ex)
            logging.error('Exception sending number to: '  + subscriber.sms_number + ' - ' + str(ex))
        ret.append(row)
    expiring_subscribers.update(active=False)
    return ret


def send_todays_texts():
    ret = []
    thought = get_todays_thought()
    for subscriber in Subscriber.objects.filter(active=True):
        row = {'to': subscriber, 'action': 'expiration'}
        try:
            send_text(subscriber, thought.thought_text, thought.post_id)
            row['result'] = 'Success'
        except DuplicateTextException:
            row['result'] = 'Duplicate'
        except TwilioRestException as ex:
            row['result'] = 'Exception: ' + str(ex)
            logging.error('Exception sending number to: '  + subscriber.sms_number + ' - ' + str(ex))
        ret.append(row)
    return ret


class DuplicateTextException(Exception):
    pass
