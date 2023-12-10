from django.db import models


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("Account", on_delete=models.CASCADE)
    type = models.CharField(max_length=255)
    date = models.DateField()
    amount = models.FloatField()
    description = models.CharField(max_length=255)
    related_fee = models.ForeignKey(
        "Fee", on_delete=models.CASCADE, null=True, blank=True
    )
