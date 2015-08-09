import logging
from django.conf import settings
from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from texts.models import Subscriber
from util import texter

from texts import models

# Create your views here.
from util.texter import get_thought, send_text


def home(request):
    return render(request, 'home.html')

# Create your views here.
def new_home(request):
    return render(request, 'newhome.html')

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
        send_text(subscriber, thought.title, thought.id)
    return HttpResponse(ret, 'text/plain')

def subscribe(request):
    if request.method == 'POST':
        sms_number = request.POST.get('sms_number', None)
        try:
            subscriber = models.Subscriber.objects.create(sms_number=sms_number)
        except IntegrityError:
            return HttpResponse('You\'re already subscribed, yo.')
        texter.send_initial_text(subscriber)
        return HttpResponse('Cool, you\'re subscribed.')
    return HttpResponseRedirect("/")

