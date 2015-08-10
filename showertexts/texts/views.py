import logging
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from twilio import TwilioRestException
from texts.models import Subscriber
from util import texter

from texts import models

from util.texter import get_thought, send_text, DuplicateTextException


def landing(request):
    return render(request, 'landing.html')

def trigger(request):
    trigger_pass = request.GET.get('p', None)
    if trigger_pass != settings.TRIGGER_PASSWORD:
        return HttpResponse('Please provide the correct trigger password', 'text/plain')

    ret = ""
    thought = get_thought()
    ret += 'Today\'s thought: ' + thought.title + '\n'
    ret += thought.url + '\n'
    for subscriber in Subscriber.objects.filter(active=True):
        ret += 'Sending text to: ' + str(subscriber) + "\n"
        try:
            send_text(subscriber, thought.title, thought.id)
            ret += ' - Success\n'
        except DuplicateTextException:
            ret += ' - Duplicate text. Won\'t send.\n'
        except TwilioRestException as ex:
            logging.error('Exception sending number to: '  + subscriber.sms_number + ' - ' + str(ex))
            ret += ' - Exception sending text: ' + str(ex) + '\n'
    return HttpResponse(ret, 'text/plain')

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
        texter.send_initial_text(subscriber)
        return HttpResponse('Cool! Check your phone!')
    return HttpResponseRedirect("/")

def count(request):
    subscriber_count = Subscriber.objects.count()
    return HttpResponse(str(subscriber_count), 'text/plain')
