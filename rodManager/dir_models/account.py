from django.db import models

from rodManager.users.manager import CustomUserManager


from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    username = None
    REQUIRED_FIELDS = []
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    permission = models.IntegerField()

    USERNAME_FIELD = "email"
    objects = CustomUserManager()
    def __str__(self):
        return self.email