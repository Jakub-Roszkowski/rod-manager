from django.contrib.auth.models import AbstractUser
from django.db import models
from rest_framework import serializers 

from rodManager.users.manager import CustomUserManager


class Account(AbstractUser):
    username = None
    REQUIRED_FIELDS = ["first_name", "last_name"]
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    phone = models.CharField(max_length=20, blank=True, null=True)
    objects = CustomUserManager()
    created_by_google = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class AccountNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["first_name", "last_name", "id"]