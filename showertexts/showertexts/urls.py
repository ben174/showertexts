from django.conf.urls import include, url
from django.contrib import admin
import texts.views

urlpatterns = [
    url(r'^$', texts.views.new_home),
    url(r'^subscribe$', texts.views.subscribe),
    url(r'^count$', texts.views.count),
    url(r'^new$', texts.views.home),
    url(r'^trigger$', texts.views.trigger),
    url(r'^admin/', include(admin.site.urls)),
]
