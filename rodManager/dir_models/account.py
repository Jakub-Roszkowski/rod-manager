from django.db import models

from rodManager.users.manager import CustomUserManager


from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    username = None
    REQUIRED_FIELDS = ["first_name", "last_name"]
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    phone = models.CharField(max_length=20, blank=True, null=True)
    objects = CustomUserManager()

    def __str__(self):
        return self.email
