from django.conf.urls import patterns, url
from django.views.generic import ListView
from eventbook.models import Event

urlpatterns = patterns('',
    # Index
    url('^$', ListView.as_view(
        model=Event,
        )),
)