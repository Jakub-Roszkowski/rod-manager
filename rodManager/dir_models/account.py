from django.db import models

from rodManager.users.manager import CustomUserManager


from django.contrib.auth.models import AbstractUser

class Account(AbstractUser):
    username = None
    REQUIRED_FIELDS = ["first_name", "last_name"]
    email = models.EmailField(unique=True)
    USERNAME_FIELD = "email"
    objects = CustomUserManager()
    def __str__(self):
        return self.email