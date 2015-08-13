import logging
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from texts.models import Subscriber
from twilio import TwilioRestException
from util import texter

from texts import models
from util.showerthoughts import get_todays_thought
from util.texter import DuplicateTextException


def landing(request):
    return render(request, 'landing.html')


def trigger(request):
    trigger_pass = request.GET.get('p', None)
    if trigger_pass != settings.TRIGGER_PASSWORD:
        return HttpResponse('Please provide the correct trigger password', 'text/plain')

    ret = texter.send_todays_texts()
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
        try:
            subscriber = models.Subscriber.objects.create(sms_number=sms_number)
        except IntegrityError:
            return HttpResponse('You\'re already subscribed, yo.')
        try:
            texter.send_initial_text(subscriber)
        except TwilioRestException as e:
            return HttpResponse('I couldn\'t send a text to that number! (' + str(e.msg) + ')', 'text/plain')
        except DuplicateTextException as e:
            return HttpResponse('I think you are already subscribed.')
        except Exception as e:
            logging.error('Exception sending number to: '  + subscriber.sms_number + ' - ' + str(e))
            return HttpResponse(str(e), 'text/plain')
        return HttpResponse('Cool! Check your phone!')
    return HttpResponseRedirect("/")


def count(request):
    subscriber_count = Subscriber.objects.filter(active=True).count()
    return HttpResponse(str(subscriber_count), 'text/plain')
