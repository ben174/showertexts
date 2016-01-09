import logging
import datetime

from django.conf import settings
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

from texts.models import TextSend, Subscriber
from util.showerthoughts import get_todays_thought


class Texter(object):
    def __init__(self):
        self.client = TwilioRestClient(settings.TWILIO_SID, settings.TWILIO_TOKEN)

    def send_text(self, subscriber, message, post_id):
        if TextSend.objects.filter(subscriber=subscriber, post_id=post_id).exists():
            logging.warning('Attempted to send a duplicate text. Won\'t do it.')
            raise DuplicateTextException()
        try:
            self.client.messages.create(
                to=subscriber.sms_number,
                from_=settings.TWILIO_NUMBER,
                body=message,
            )
        except TwilioRestException as e:
            logging.error('Exception sending number to: ' + subscriber.sms_number + ' - ' + str(e))
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

    def send_todays_texts(self):
        ret = []
        thought = get_todays_thought()
        for subscriber in Subscriber.objects.filter(active=True):
            row = {'to': subscriber, 'action': 'showertext'}
            message = thought.thought_text
            post_id = thought.post_id
            if subscriber.expired:
                row['action'] = 'expiration'
                subscriber.active = False
                subscriber.save()
                message = 'HOUSE KEEPING! I\'m clearing out old numbers to make room for more. If you like these, ' \
                          'please resubscribe for free! http://www.showertexts.com'
                post_id = 'EXP-' + str(datetime.date.today())
            try:
                self.send_text(subscriber, message, post_id)
                row['result'] = 'Success'
            except DuplicateTextException:
                row['result'] = 'Duplicate'
            except TwilioRestException as ex:
                row['result'] = 'Exception: ' + str(ex)
                logging.error('Exception sending number to: ' + subscriber.sms_number + ' - ' + str(ex))
            ret.append(row)
        return ret


class DuplicateTextException(Exception):
    pass
