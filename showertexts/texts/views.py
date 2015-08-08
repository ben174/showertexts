from django.shortcuts import render
from django.http import HttpResponse
from util import texter

from texts import models

# Create your views here.
def home(request):
    return render(request, 'home.html') 

def subscribe(request):
    if request.method == 'POST':
        sms_number = request.POST.get('sms_number', None)
        subscriber = models.Subscriber.objects.create(sms_number=sms_number)
        texter.send_initial_text(subscriber)
        return HttpResponse("Cool, you're subscribed")
    return HttpResponse("Please, POST.")

