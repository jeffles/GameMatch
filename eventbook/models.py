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
