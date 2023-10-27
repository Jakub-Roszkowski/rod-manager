from django.db import models


class Vote(models.Model):
    id = models.AutoField(primary_key=True)
    type = models.FloatField()
    end_date = models.DateTimeField()
    start_date = models.DateTimeField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    options = models.TextField()
