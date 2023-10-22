from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=255)
    id = models.AutoField(primary_key=True)
    public = models.BooleanField(default=False)
    description = models.TextField()
    color = models.CharField(max_length=255)
    times_used = models.IntegerField()