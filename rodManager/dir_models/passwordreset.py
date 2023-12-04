from django.db import models
from rest_framework import serializers


class PasswordReset(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=255)
    valid_until = models.DateTimeField()
