from django.test import TestCase, LiveServerTestCase, Client
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
        self.assertEqual(only_event.title, 'My first event')
        self.assertEqual(only_event.text, 'This is my first game night')
        self.assertEqual(only_event.attendees, 'Jed and Jimmy')
        self.assertEqual(only_event.location, "Jeff's house")
        self.assertEqual(only_event.pub_date.day, event.pub_date.day)
        self.assertEqual(only_event.pub_date.month, event.pub_date.month)
        self.assertEqual(only_event.pub_date.year, event.pub_date.year)
        self.assertEqual(only_event.pub_date.hour, event.pub_date.hour)
        self.assertEqual(only_event.pub_date.minute, event.pub_date.minute)
        self.assertEqual(only_event.pub_date.second, event.pub_date.second)

        self.assertEqual(only_event.start_date.day, event.start_date.day)
        self.assertEqual(only_event.start_date.month, event.start_date.month)
        self.assertEqual(only_event.start_date.year, event.start_date.year)
        self.assertEqual(only_event.start_date.hour, event.start_date.hour)
        self.assertEqual(only_event.start_date.minute, event.start_date.minute)
        self.assertEqual(only_event.start_date.second, event.start_date.second)

        self.assertEqual(only_event.end_time.hour, event.end_time.hour)
        self.assertEqual(only_event.end_time.minute, event.end_time.minute)
        self.assertEqual(only_event.end_time.second, event.end_time.second)

class AdminTest(LiveServerTestCase):
    fixtures = ['users.json']

    def test_login(self):
        # Create client
        c = Client()

        # Get login page
        response = c.get('/admin/', follow=True)

        # Check response code
        self.assertEqual(response.status_code, 200)

        # Check 'Log in' in response
        self.assertTrue('Log in' in response.content)

        # Log the user in
        c.login(username='bobsmith', password="password")

        # Check response code
        response = c.get('/admin/', follow=True)
        self.assertEquals(response.status_code, 200)

        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content)

    def test_logout(self):
        # Create client
        c = Client()

        # Log in
        c.login(username='bobsmith', password="password")

        # Check response code
        response = c.get('/admin/', follow=True)
        self.assertEquals(response.status_code, 200)

        # Check 'Log out' in response
        self.assertTrue('Log out' in response.content)

        # Log out
        c.logout()

        # Check response code
        response = c.get('/admin/', follow=True)
        self.assertEquals(response.status_code, 200)

        # Check 'Log in' in response
        self.assertTrue('Log in' in response.content)