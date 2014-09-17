from django.test import TestCase
from django.utils import timezone
from eventbook.models import Event

class EventTest(TestCase):
    def test_create_event(self):
        # Create the event
        event = Event()

        # Set the attributes
        event.title = 'My first event'
        event.text = 'This is my first game night'
        event.pub_date = timezone.now()
        event.start_date = timezone.now()
        event.end_time = timezone.now().time()
        event.attendees = 'Jed and Jimmy'
        event.location = "Jeff's house"

        # Save it
        event.save()

        # Check we can find it
        all_events = Event.objects.all()
        self.assertEquals(len(all_events), 1)
        only_event = all_events[0]
        self.assertEquals(only_event, event)

        # Check attributes
        self.assertEquals(only_event.title, 'My first event')
        self.assertEquals(only_event.text, 'This is my first game night')
        self.assertEquals(only_event.attendees, 'Jed and Jimmy')
        self.assertEquals(only_event.location, "Jeff's house")
        self.assertEquals(only_event.pub_date.day, event.pub_date.day)
        self.assertEquals(only_event.pub_date.month, event.pub_date.month)
        self.assertEquals(only_event.pub_date.year, event.pub_date.year)
        self.assertEquals(only_event.pub_date.hour, event.pub_date.hour)
        self.assertEquals(only_event.pub_date.minute, event.pub_date.minute)
        self.assertEquals(only_event.pub_date.second, event.pub_date.second)

        self.assertEquals(only_event.start_date.day, event.start_date.day)
        self.assertEquals(only_event.start_date.month, event.start_date.month)
        self.assertEquals(only_event.start_date.year, event.start_date.year)
        self.assertEquals(only_event.start_date.hour, event.start_date.hour)
        self.assertEquals(only_event.start_date.minute, event.start_date.minute)
        self.assertEquals(only_event.start_date.second, event.start_date.second)

        self.assertEquals(only_event.end_time.hour, event.end_time.hour)
        self.assertEquals(only_event.end_time.minute, event.end_time.minute)
        self.assertEquals(only_event.end_time.second, event.end_time.second)
