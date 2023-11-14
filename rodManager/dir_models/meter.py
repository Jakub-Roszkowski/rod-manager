from django.db import models


class Meter(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    type = models.CharField(max_length=200)
    adress = models.CharField(max_length=200)
    garden = models.ForeignKey()