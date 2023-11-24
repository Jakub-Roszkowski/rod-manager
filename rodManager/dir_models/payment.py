from django.db import models


class Payment(models.Model):
    leaseholderID = models.CharField(max_length=255)
    date = models.DateField()
    amount = models.FloatField()
    description = models.CharField(max_length=255)
    required_fields = ["leaseholderID", "date", "amount"]
