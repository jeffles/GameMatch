from django.conf.urls import patterns, url
from django.views.generic import ListView, DetailView
from eventbook.models import Event
from eventbook.views import EventCreate, EventUpdate, ShowFriends

urlpatterns = patterns('',
    # Index
    url(r'^(?P<page>\d+)?/?$', ListView.as_view(
        model=Event,
        paginate_by=5,
        ),
        name='index'
        ),

    # Individual events
    url(r'^create/?$', EventCreate.as_view(), name='create'),
    url(r'^showfriends/?', ShowFriends, name='showfriends'),

    # Individual events
    url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/?$', DetailView.as_view(
        model=Event,
        ),
        name='event'
        ),

    # Individual events
    url(r'^(?P<pub_date__year>\d{4})/(?P<pub_date__month>\d{1,2})/(?P<slug>[a-zA-Z0-9-]+)/update/?$',
        EventUpdate.as_view(), name='update'),
)