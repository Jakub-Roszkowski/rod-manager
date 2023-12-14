from django.db import models

from rodManager.dir_models.account import Account


class NotificationType(models.TextChoices):
    INFO = "Info"
    WARNING = "Warning"
    ERROR = "Error"


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("Account", on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    date = models.DateTimeField()
    text = models.TextField()
    is_read = models.BooleanField(default=False)
    is_email_sent = models.BooleanField(default=False)
