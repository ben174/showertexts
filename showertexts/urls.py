from django.conf.urls import include, url
from django.contrib import admin
import texts.views

urlpatterns = [
    url(r'^$', texts.views.landing),
    url(r'^subscribe$', texts.views.subscribe),
    url(r'^count$', texts.views.count),
    url(r'^trigger$', texts.views.trigger),
    url(r'^today$', texts.views.today),
    url(r'^alt$', texts.views.alternate),
    url(r'^queue$', texts.views.queue),
    url(r'^random$', texts.views.random),
    url(r'^admin/', include(admin.site.urls)),
]
