from django.db import models
from rest_framework import serializers


class PasswordReset(models.Model):
    user = models.ForeignKey("Account", on_delete=models.CASCADE)
    token = models.UUIDField()
    valid_until = models.DateTimeField()
