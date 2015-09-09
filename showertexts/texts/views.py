import logging
import datetime
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from texts.models import Subscriber
from twilio import TwilioRestException
from util import texter

from util.showerthoughts import get_todays_thought
from util.texter import DuplicateTextException, send_text


def landing(request):
    return render(request, 'landing.html')


def trigger(request):
    trigger_pass = request.GET.get('p', None)
    if trigger_pass != settings.TRIGGER_PASSWORD:
        return HttpResponse('Please provide the correct trigger password', 'text/plain')

    ret = texter.send_todays_expirations()
    ret += texter.send_todays_texts()
    return HttpResponse(ret, 'text/plain')

def today(request):
    thought = get_todays_thought()
    return HttpResponse(thought.thought_text, 'text/plain')

@csrf_exempt
def subscribe(request):
    if request.method == 'POST':
        sms_number = request.POST.get('sms_number', None)
        if not sms_number:
            return HttpResponse('You sent nothing yo.')
        sms_number = filter(str.isdigit, str(sms_number))
        subscriber, created = Subscriber.objects.get_or_create(sms_number=sms_number)
        if not created:
            if subscriber.expired:
                # yay! a renewal
                subscriber.expired = False
                subscriber.date_renewed = datetime.datetime.now()
                subscriber.save()
                texter.send_initial_text(subscriber)
                return HttpResponse('Welcome back! Check your phone!')
            elif not subscriber.active:
                # technically they could be blacklisted, but i can't do anything about that
                return HttpResponse('Did you reply STOP? Reply START and try again.')
            else:
                return HttpResponse('You\'re already subscribed, yo.')
        try:
            message = "Cool! Welcome to ShowerTexts.com! You'll start receiving Shower Texts daily. " \
                      "Reply STOP at any time if you get sick of them. " \
                      "Your first one will follow..."
            send_text(subscriber, message, 'initial')
        except TwilioRestException as e:
            logging.error('Exception sending number to: '  + subscriber.sms_number + ' - ' + str(e))
            return HttpResponse('I couldn\'t send a text to that number! (' + str(e.msg) + ')', 'text/plain')
        except DuplicateTextException:
            logging.warning('Duplicate welcome text.')
        thought = get_todays_thought()
        try:
            send_text(subscriber, thought.thought_text, thought.post_id)
        except TwilioRestException as e:
            logging.error('Exception sending number to: '  + subscriber.sms_number + ' - ' + str(e))
            return HttpResponse('I couldn\'t send a text to that number! (' + str(e.msg) + ')', 'text/plain')
        except DuplicateTextException:
            logging.error('Duplicate initial thought. Shouldn\'t happen - odd.')
        return HttpResponse('Cool! Check your phone!')
    return HttpResponseRedirect("/")


def count(request):
    subscriber_count = Subscriber.objects.filter(active=True, expired=False).count()
    return HttpResponse(str(subscriber_count), 'text/plain')
