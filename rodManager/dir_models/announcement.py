from django.db import models


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    tags = models.ManyToManyField("Tag", blank=True)
    images = models.ManyToManyField("Image", blank=True)
