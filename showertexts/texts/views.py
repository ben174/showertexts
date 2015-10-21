from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

from texts.models import Subscriber
from util.showerthoughts import get_todays_thought, get_submissions, choose_alternate, random_thought
from util.subscription import subscribe as subscribe_number
from util.texter import Texter


def requires_trigger(view_func):
    """
    A decorator which checks for a query parameter containing the trigger password.
    The trigger password is stored in settings.py, but overridden in production by
    a secret environment variable.

    """
    def inner(request):
        trigger_pass = request.GET.get('p', None)
        if trigger_pass != settings.TRIGGER_PASSWORD:
            return HttpResponse('Please provide the correct trigger password', 'text/plain')
        return view_func(request)
    return inner


def landing(request):
    """ Landing page """
    return render(request, 'landing.html')


@requires_trigger
def trigger(request):
    """ A URL which invokes a trigger to send out today's texts. """
    texter = Texter()
    ret = texter.send_todays_texts()
    return HttpResponse(ret, 'text/plain')


def today(request):
    """ Returns todays selected post in plain text. Used for Alexa endpoint. """
    ret = cache.get('todays_thought_text')
    if not ret:
        thought = get_todays_thought()
        ret = thought.thought_text
        cache.set('todays_thought_text', ret, 60 * 15)
    return HttpResponse(ret, 'text/plain')


def random(request):
    """
    Returns a random thought from our history in plain text.
    Might use for an Alexa endpoint someday

    """
    thought = random_thought()
    return HttpResponse(thought.thought_text, 'text/plain')


@requires_trigger
def alternate(request):
    """ Allows an admin to select an alternate post from today's front page. """
    trigger_pass = request.GET.get('p', None)
    alt_id = request.GET.get('s', None)
    if alt_id:
        choose_alternate(alt_id)
        return HttpResponseRedirect('/today')
    return render(request, 'alternates.html', {
        'today': get_todays_thought().thought_text,
        'submissions': get_submissions(),
        'trigger': trigger_pass,
    })


@csrf_exempt
def subscribe(request):
    """
    New subscriptions are posted here.
    Returns a plain text response message which can be returned to the user.

    """
    if request.method == 'POST':
        sms_number = request.POST.get('sms_number', None)
        welcome_message = subscribe_number(sms_number)
        return HttpResponse(welcome_message, 'text/plain')
    return HttpResponseRedirect("/")


def count(request):
    """
    Returns a plain text count of /active/ subscribers. It used to be displayed on the
    home page but I removed it. This end point is still accessible to the public
    for those who are so inclined.

    """
    subscriber_count = Subscriber.objects.filter(active=True).count()
    return HttpResponse(str(subscriber_count), 'text/plain')
