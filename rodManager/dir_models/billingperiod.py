from django.db import models


class BillingPeriod(models.Model):
    id = models.AutoField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    payment_date = models.DateField()
    is_confirmed = models.BooleanField(default=False)
    confimation_date = models.DateTimeField(null=True, blank=True)
