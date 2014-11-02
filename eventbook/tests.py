from django.core.urlresolvers import reverse
from django.test import TestCase, LiveServerTestCase, Client
from django.utils import timezone
from eventbook.models import Event
from eventbook.models import Game
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
import factory.django


# Factories
class SiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Site
        django_get_or_create = (
            'name',
            'domain'
        )

    name = 'example.com'
    domain = 'example.com'


class HostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username', 'email', 'password',)

    username = 'testuser'
    email = 'user@example.com'
    password = 'password'


class EventFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Event
        django_get_or_create = (
            'title',
            'text',
            'pub_date',
            'start_date',
            'end_time',
            'attendees',
            'location',
            'slug',
            'host',
            'site'
        )

    title = 'My first event'
    text = 'This is my first game night'
    slug = 'my-first-event'
    pub_date = timezone.localtime(timezone.now())
    host = factory.SubFactory(HostFactory)
    site = factory.SubFactory(SiteFactory)
    start_date = timezone.localtime(timezone.now())
    end_time = timezone.localtime(timezone.now()).time()
    attendees = 'Jed and Jimmy'
    location = 'Jeff'


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game
        django_get_or_create = (
            'id',
            'name',
            'yearpublished',
            'minplayers',
            'maxplayers',
            'playingtime',
#            'families',
#            'categories',
#            'mechanics',
#            'designers',
#            'artists',
#            'publishers',
#            'categories',
            'thumbnail',
            'image',
            'description'
        )

    id = '359'
    name = 'Honeybears'
    yearpublished = '1998'
    minplayers = 3
    maxplayers = 5
    playingtime = '30 minutes'
#            'families',
#            'categories',
#            'mechanics',
#            'designers',
#            'artists',
#            'publishers',
#            'categories',
    thumbnail = 'http://cf.geekdo-images.com/images/pic199026_t.jpg'
    image = 'http://cf.geekdo-images.com/images/pic199026_md.jpg'
    description = 'Card game with a racing track by Reiner Knizia.'


class EventTest(TestCase):
    def test_create_event(self):

        event = EventFactory()

        # Check we can find it
        all_events = Event.objects.all()
        self.assertEquals(len(all_events), 1)
        only_event = all_events[0]
        self.assertEquals(only_event, event)

        # Check attributes
        self.assertEqual(only_event.title, 'My first event')
        self.assertEqual(only_event.text, 'This is my first game night')
        self.assertEqual(only_event.slug, 'my-first-event')
        self.assertEqual(only_event.site.name, 'example.com')
        self.assertEqual(only_event.site.domain, 'example.com')
        self.assertEqual(only_event.attendees, 'Jed and Jimmy')
        self.assertEqual(only_event.location, "Jeff")
        self.assertEqual(timezone.localtime(only_event.pub_date).day, timezone.localtime(event.pub_date).day)
        self.assertEqual(only_event.pub_date.month, event.pub_date.month)
        self.assertEqual(only_event.pub_date.year, event.pub_date.year)
        self.assertEqual(timezone.localtime(only_event.pub_date).hour, timezone.localtime(event.pub_date).hour)
        self.assertEqual(only_event.pub_date.minute, event.pub_date.minute)
        self.assertEqual(only_event.pub_date.second, event.pub_date.second)

        self.assertEqual(timezone.localtime(only_event.start_date).day, timezone.localtime(event.start_date).day)
        self.assertEqual(only_event.start_date.month, event.start_date.month)
        self.assertEqual(only_event.start_date.year, event.start_date.year)
        self.assertEqual(timezone.localtime(only_event.start_date).hour, timezone.localtime(event.start_date).hour)
        self.assertEqual(only_event.start_date.minute, event.start_date.minute)
        self.assertEqual(only_event.start_date.second, event.start_date.second)

        self.assertEqual(only_event.end_time.hour, event.end_time.hour)
        self.assertEqual(only_event.end_time.minute, event.end_time.minute)
        self.assertEqual(only_event.end_time.second, event.end_time.second)

        self.assertEqual(only_event.host.username, 'testuser')
        self.assertEqual(only_event.host.email, 'user@example.com')


class GameTest(TestCase):
    def test_create_game(self):

        game = GameFactory()

        # Check we can find it
        all_games = Game.objects.all()
        self.assertEquals(len(all_games), 1)
        only_game = all_games[0]
        self.assertEquals(only_game, game)

        # Check attributes
        self.assertEqual(only_game.id, '359')
        self.assertEqual(only_game.name, 'Honeybears')
        self.assertEqual(only_game.yearpublished, '1998')
        self.assertEqual(only_game.minplayers, 3)
        self.assertEqual(only_game.maxplayers, 5)
        self.assertEqual(only_game.playingtime, '30 minutes')
        self.assertEqual(only_game.thumbnail, 'http://cf.geekdo-images.com/images/pic199026_t.jpg')
        self.assertEqual(only_game.image, 'http://cf.geekdo-images.com/images/pic199026_md.jpg')
        self.assertEqual(only_game.description, 'Card game with a racing track by Reiner Knizia.')


class BaseAcceptanceTest(LiveServerTestCase):
    def setUp(self):
        self.client = Client()


class AdminTest(BaseAcceptanceTest):
    fixtures = ['users.json']

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
            'location': "Jeff's house",
            'slug': 'my-first-post',
            'site': '1'
        },
        follow=True
        )
        self.assertEquals(response.status_code, 200)

        self.assertTrue('added successfully' in response.content)
        all_events = Event.objects.all()
        self.assertEquals(len(all_events), 1)

    def test_edit_event(self):
        event = EventFactory()

        # Check event amended
        all_events = Event.objects.all()
        self.assertEquals(len(all_events), 1)
        only_event = all_events[0]
        self.assertEquals(only_event.title, 'My first event')
        self.assertEquals(only_event.text, 'This is my first game night')

        self.client.login(username='bobsmith', password="password")

        response = self.client.get('/admin/eventbook/event/')
        self.assertEquals(response.status_code, 200)

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
            'location': "Jeff's house",
            'slug': 'my-first-post',
            'site': '1'
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

        event = EventFactory()

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


class PostViewTest(BaseAcceptanceTest):

    def test_index(self):
        event = EventFactory()

        # Check new event saved
        all_events = Event.objects.all()
        self.assertEquals(len(all_events), 1)

        # Fetch the index
        response = self.client.get(reverse('eventbook:index'))
        self.assertEquals(response.status_code, 200)

        self.assertTrue(event.title in response.content)
        self.assertTrue(event.text in response.content)
        self.assertTrue(str(event.pub_date.year) in response.content)
        self.assertTrue(event.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(event.pub_date.day) in response.content)
        self.assertTrue(str(event.start_date.year) in response.content)
        self.assertTrue(event.start_date.strftime('%b') in response.content)
        self.assertTrue(str(event.start_date.day) in response.content)
#        self.assertTrue(event.start_date.strftime('%c') in response.content)
#        self.assertTrue(event.end_time.strftime('%X') in response.content)
        self.assertTrue(event.attendees in response.content)
        self.assertTrue(event.location in response.content)

    def test_event_page(self):
        event = EventFactory()

        all_events = Event.objects.all()
        self.assertEquals(len(all_events), 1)
        only_event = all_events[0]
        self.assertEquals(only_event, event)

        # Fetch the event
        event_url = only_event.get_absolute_url()
        response = self.client.get(event_url)
        self.assertEquals(response.status_code, 200)

        self.assertTrue(event.title in response.content)
        self.assertTrue(event.text in response.content)
        self.assertTrue(str(event.pub_date.year) in response.content)
        self.assertTrue(event.pub_date.strftime('%b') in response.content)
        self.assertTrue(str(event.pub_date.day) in response.content)
        self.assertTrue(str(event.start_date.year) in response.content)
        self.assertTrue(event.start_date.strftime('%b') in response.content)
        self.assertTrue(str(event.start_date.day) in response.content)
#        self.assertTrue(event.start_date.strftime('%H:%M') in response.content)
#        self.assertTrue(event.end_time.strftime('%H:%M') in response.content)
        self.assertTrue(event.attendees in response.content)
        self.assertTrue(event.location in response.content)