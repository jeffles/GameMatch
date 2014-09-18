from django.db import models


# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField()
    text = models.TextField()
    start_date = models.DateTimeField()
    end_time = models.TimeField()
    attendees = models.TextField()
    location = models.TextField()
    slug = models.SlugField(max_length=40, unique=True)

    def get_absolute_url(self):
        return "/%s/%s/%s/%s/" % (self.pub_date.year, self.pub_date.month, self.pub_date.day, self.slug)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ["-pub_date"]

