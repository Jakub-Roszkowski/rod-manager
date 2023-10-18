from django.db import models

class Reminder(models.Model):
    date = models.DateField()
    time = models.TimeField()
    message = models.TextField()
    account = models.ForeignKey('Account', on_delete=models.CASCADE)
