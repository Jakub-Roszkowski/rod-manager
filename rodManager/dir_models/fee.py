from django.db import models
from rest_framework import serializers


class FeeFeeType(models.TextChoices):
    LEASE = "Lease"
    UTILITY = "Utility"
    ADDITIONAL = "Additional"


class FeeCalculationType(models.TextChoices):
    PERGARDEN = "Za działkę"
    PERMETER = "Za metr"


class Fee(models.Model):
    id = models.AutoField(primary_key=True)
    billing_period = models.ForeignKey(
        "BillingPeriod", on_delete=models.CASCADE, null=True, blank=True
    )
    fee_type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    calculation_type = models.CharField(max_length=255)
    value = models.FloatField()

    def __str__(self):
        return self.name
