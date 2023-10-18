from django.db import models

class Vote(models.Model):
    end_date = models.DateTimeField()
    start_date = models.DateTimeField()
    title = models.CharField(max_length=200)
    description = models.TextField()
    options = models.TextField()
    type = models.FloatField()
    id = models.AutoField(primary_key=True)