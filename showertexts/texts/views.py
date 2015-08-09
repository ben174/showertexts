from django.db import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from util import texter

from texts import models

# Create your views here.
def home(request):
    return render(request, 'home.html')

# Create your views here.
def new_home(request):
    return render(request, 'newhome.html')

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

