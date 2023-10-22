from django.db import models


class Announcement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    id = models.AutoField(primary_key=True)