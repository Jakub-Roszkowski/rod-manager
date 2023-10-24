from django.db import models


class Announcement(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateTimeField()
    tags = models.ManyToManyField("Tag")
    pictures = models.ManyToManyField("Picture")
