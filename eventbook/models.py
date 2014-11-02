from django.db import models
from django.contrib.auth.models import User
from django.contrib.sites.models import Site


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    text = models.TextField()
    start_date = models.DateTimeField()
    end_time = models.TimeField()
    attendees = models.TextField()
    location = models.TextField()
    host = models.ForeignKey(User)
    slug = models.SlugField(max_length=40, unique=True)
    site = models.ForeignKey(Site)

    def get_absolute_url(self):
        return "/%s/%s/%s/" % (self.pub_date.year, self.pub_date.month,  self.slug)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["-pub_date"]


class Game(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=255)
    yearpublished = models.CharField(max_length=5)
    minplayers = models.IntegerField()
    maxplayers = models.IntegerField()
    playingtime = models.CharField(max_length=50)
#            'families',
#            'categories',
#            'mechanics',
#            'designers',
#            'artists',
#            'publishers',
#            'categories',
    thumbnail = models.URLField()
    image = models.URLField()
    description = models.TextField()

    def get_absolute_url(self):
        return self.id

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]