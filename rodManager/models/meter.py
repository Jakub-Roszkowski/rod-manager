from django.db import models


class Meter(models.Model):
    adress = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    id = models.CharField(max_length=200, primary_key=True)