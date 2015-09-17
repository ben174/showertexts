from django.conf.urls import include, url
from django.contrib import admin
import texts.views

urlpatterns = [
    url(r'^$', texts.views.landing),
    url(r'^subscribe$', texts.views.subscribe),
    url(r'^count$', texts.views.count),
    url(r'^clear$', texts.views.clear),
    url(r'^trigger$', texts.views.trigger),
    url(r'^today$', texts.views.today),
    url(r'^admin/', include(admin.site.urls)),
]
