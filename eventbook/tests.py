from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from eventbook.models import Event


class EventTest(TestCase):
    def test_create_event(self):
        event = Event()

        event.title = 'My first event'
        event.text = 'This is my first game night'
        event.pub_date = timezone.now()
        event.start_date = timezone.now()
        event.end_time = timezone.now().time()
        event.attendees = 'Jed and Jimmy'
        event.location = "Jeff's house"
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
    reset_sequences = True

    def setUp(self):
        self.client = Client()

    def test_login(self):
        response = self.client.get('/admin/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Log in' in response.content)
        self.client.login(username='bobsmith', password="password")
        response = self.client.get('/admin/', follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Log out' in response.content)

    def test_logout(self):
        self.client.login(username='bobsmith', password="password")
        response = self.client.get('/admin/', follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Log out' in response.content)
        self.client.logout()
        response = self.client.get('/admin/', follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertTrue('Log in' in response.content)

    def test_create_event(self):
        self.client.login(username='bobsmith', password="password")
        response = self.client.get('/admin/eventbook/event/add/')
        self.assertEquals(response.status_code, 200)

        response = self.client.post('/admin/eventbook/event/add/', {
            'title': 'My first event',
            'text': 'This is my first game night',
            'pub_date_0': '2013-12-28',
            'pub_date_1': '22:00:04',
            'start_date_0': '2013-12-28',
            'start_date_1': '22:00:04',
            'end_time': '23:00:04',
            'attendees': 'Jed and Jimmy',
            'location': "Jeff's house"
        },
        follow=True
        )
        self.assertEquals(response.status_code, 200)

        self.assertTrue('added successfully' in response.content)
        all_events = Event.objects.all()
        self.assertEquals(len(all_events), 1)

    def test_edit_event(self):
        event = Event()
        event.title = 'My first event'
        event.text = 'This is my first game night'
        event.pub_date = timezone.now()
        event.start_date = timezone.now()
        event.end_time = timezone.now().time()
        event.attendees = 'Jed and Jimmy'
        event.location = 'Jeff'
        event.save()

        # Check event amended
        all_events = Event.objects.all()
        self.assertEquals(len(all_events), 1)
        only_event = all_events[0]
        self.assertEquals(only_event.title, 'My first event')
        self.assertEquals(only_event.text, 'This is my first game night')

        self.client.login(username='bobsmith', password="password")

        response = self.client.get('/admin/eventbook/event/')
        self.assertEquals(response.status_code, 200)

        #TODO figure out why it is getting created as 2 instead of 1
        response = self.client.get('/admin/eventbook/event/'+str(only_event.pk)+'/')
        self.assertEquals(response.status_code, 200)

        response = self.client.post('/admin/eventbook/event/'+str(only_event.pk)+'/', {
            'title': 'My second event',
            'text': 'This is my second game night',
            'pub_date_0': '2013-12-28',
            'pub_date_1': '22:00:04',
            'start_date_0': '2013-12-28',
            'start_date_1': '22:00:04',
            'end_time': '23:00:04',
            'attendees': 'Jed and Jimmy',
            'location': "Jeff's house"
        },
        follow=True
        )
        self.assertEquals(response.status_code, 200)

        self.assertTrue('changed successfully' in response.content)

        # Check event amended
        all_events = Event.objects.all()
        self.assertEquals(len(all_events), 1)
        only_event = all_events[0]
        self.assertEquals(only_event.title, 'My second event')
        self.assertEquals(only_event.text, 'This is my second game night')

    def test_delete_event(self):
        event = Event()
        event.title = 'My first event'
        event.text = 'This is my first game night'
        event.pub_date = timezone.now()
        event.start_date = timezone.now()
        event.end_time = timezone.now().time()
        event.attendees = 'Jed and Jimmy'
        event.location = 'Jeff'
        event.save()

        # Check new event saved
        all_events = Event.objects.all()
        self.assertEquals(len(all_events), 1)

        # Log in
        self.client.login(username='bobsmith', password="password")

        # Delete the event
        response = self.client.post('/admin/eventbook/event/'+str(event.pk)+'/delete/', {
            'post': 'yes'
        }, follow=True)
        self.assertEquals(response.status_code, 200)

        # Check deleted successfully
        self.assertTrue('deleted successfully' in response.content)

        # Check event amended
        all_events = Event.objects.all()
        self.assertEquals(len(all_events), 0)