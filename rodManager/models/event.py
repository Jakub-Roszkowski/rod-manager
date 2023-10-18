from django.db import models
from models.announcement import Announcement

class Event(Announcement):
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    duration = models.IntegerField()
