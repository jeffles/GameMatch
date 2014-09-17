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
