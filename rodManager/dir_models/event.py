from django.db import models
from models.announcement import Announcement


class Event(Announcement):
    id = models.AutoField(primary_key=True)
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    duration = models.IntegerField()
