from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.views.generic.edit import CreateView, UpdateView
from eventbook.models import Event
import atom.data
import gdata.data
import gdata.contacts.client
import gdata.contacts.data

def home(request):
    context = RequestContext(request,
                             {'request': request,
                             'user': request.user})
    return render_to_response('eventbook/event_list.html',
                              context_instance=context)


class EventCreate(CreateView):
    template_name_suffix = '_create_form'
    model = Event
#    fields = ['title']


class EventUpdate(UpdateView):
    model = Event
#    fields = ['name']
    template_name_suffix = '_update_form'

def ShowFriends(request):

    # ...
    gd_client = gdata.contacts.client.ContactsClient(source='baldmousegames')
    feed = gd_client.GetContacts()
    for i, entry in enumerate(feed.entry):
        print '\n%s %s' % (i+1, entry.name.full_name.text)
        if entry.content:
          print '    %s' % (entry.content.text)
        # Display the primary email address for the contact.
        for email in entry.email:
          if email.primary and email.primary == 'true':
            print '    %s' % (email.address)
        # Show the contact groups that this contact is a member of.
        for group in entry.group_membership_info:
          print '    Member of group: %s' % (group.href)
        # Display extended properties.
        for extended_property in entry.extended_property:
          if extended_property.value:
            value = extended_property.value
          else:
            value = extended_property.GetXmlBlob()
          print '    Extended Property - %s: %s' % (extended_property.name, value)
    return render_to_response('eventbook/show_friends.html')

def create(request):
    context = RequestContext(request,
                             {'request': request,
                             'user': request.user})
    return render_to_response('eventbook/event_list.html',
                              context_instance=context)
