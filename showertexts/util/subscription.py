import logging
from texts.models import Subscriber
from twilio import TwilioRestException
from util.showerthoughts import get_todays_thought
from util.texter import DuplicateTextException, Texter


def subscribe(sms_number):
    if not sms_number:
        return 'You sent nothing yo.'
    sms_number = filter(str.isdigit, str(sms_number))
    subscriber, created = Subscriber.objects.get_or_create(sms_number=sms_number)
    texter = Texter()
    if not created:
        if subscriber.expired:
            # yay! a renewal
            subscriber.renew()
            subscriber.save()
            thought = get_todays_thought()
            try:
                texter.send_text(subscriber, thought.thought_text, thought.post_id)
            except TwilioRestException as e:
                subscriber.active = False
                subscriber.save()
                logging.error('Exception sending number to: ' + subscriber.sms_number + ' - ' + str(e))
                return 'I couldn\'t send a text to that number! (' + str(e.msg) + ')'
            except DuplicateTextException:
                # no prob, they already got todays message
                pass
            return 'Welcome back! Check your phone!'
        elif not subscriber.active:
            # technically they could be blacklisted, but i can't do anything about that
            return 'Did you reply STOP? Reply START and try again.'
        else:
            return 'You\'re already subscribed, yo.'
    try:
        message = "Cool! Welcome to ShowerTexts.com! You'll start receiving Shower Texts daily. " \
                  "Reply STOP at any time if you get sick of them. " \
                  "Your first one will follow..."
        texter.send_text(subscriber, message, 'initial')
    except TwilioRestException as e:
        logging.error('Exception sending number to: ' + subscriber.sms_number + ' - ' + str(e))
        return 'I couldn\'t send a text to that number! (' + str(e.msg) + ')'
    except DuplicateTextException:
        logging.warning('Duplicate welcome text.')
    thought = get_todays_thought()
    try:
        texter.send_text(subscriber, thought.thought_text, thought.post_id)
    except TwilioRestException as e:
        logging.error('Exception sending number to: ' + subscriber.sms_number + ' - ' + str(e))
        return 'I couldn\'t send a text to that number! (' + str(e.msg) + ')'
    except DuplicateTextException:
        logging.error('Duplicate initial thought. Shouldn\'t happen - odd.')
    return 'Cool! Check your phone!'