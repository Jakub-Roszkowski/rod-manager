from django.db import models


class Event(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateTimeField()
    name = models.CharField(max_length=255)
    announcement = models.OneToOneField("Announcement", on_delete=models.CASCADE)
