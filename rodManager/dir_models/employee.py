from django.db import models
from rest_framework import serializers


class Employee(models.Model):
    id = models.AutoField(primary_key=True)
    position = models.CharField(max_length=255, null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    phoneNumber = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)


