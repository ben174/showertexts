from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from texts.models import Subscriber
from util.showerthoughts import get_todays_thought
from util.subscription import subscribe as subscribe_number
from util.texter import Texter


def landing(request):
    return render(request, 'landing.html')


def trigger(request):
    trigger_pass = request.GET.get('p', None)
    if trigger_pass != settings.TRIGGER_PASSWORD:
        return HttpResponse('Please provide the correct trigger password', 'text/plain')
    texter = Texter()
    ret = texter.send_todays_texts()
    return HttpResponse(ret, 'text/plain')


def today(request):
    thought = get_todays_thought()
    return HttpResponse(thought.thought_text, 'text/plain')


@csrf_exempt
def subscribe(request):
    if request.method == 'POST':
        sms_number = request.POST.get('sms_number', None)
        welcome_message = subscribe_number(sms_number)
        return HttpResponse(welcome_message, 'text/plain')
    return HttpResponseRedirect("/")


def count(request):
    subscriber_count = Subscriber.objects.filter(active=True).count()
    return HttpResponse(str(subscriber_count), 'text/plain')
