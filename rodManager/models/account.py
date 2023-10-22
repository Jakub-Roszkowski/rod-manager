from django.db import models

from rodManager.users.manager import CustomUserManager


class Account(models.AbstractUser):
    username = None

    email = models.EmailField(primary_key=True, unique=True)
    password = models.CharField(max_length=128)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    permission = models.IntegerField()

    USERNAME_FIELD = "email"
    objects = CustomUserManager()
    def __str__(self):
        return self.email