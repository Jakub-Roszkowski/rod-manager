from django.db import models


class Record(models.Model):
    meter = models.ForeignKey("Meter", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    value = models.FloatField()
