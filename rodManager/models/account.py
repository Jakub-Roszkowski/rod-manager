from django.db import models


class Account(models.Model):
    email = models.EmailField(primary_key=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    permission = models.IntegerField()