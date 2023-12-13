from django.db import models

from rodManager.dir_models.account import Account


class PaymentType(models.TextChoices):
    BILLPAYMENT = "BillPayment"
    CORRECTION = "Correction"
    PAYMENT = "Payment"
    INDIVIDUAL = "Individual"


class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("Account", on_delete=models.CASCADE)
    type = models.CharField(
        max_length=20,
        choices=PaymentType.choices,
        default=PaymentType.PAYMENT,
    )
    date = models.DateField()
    amount = models.FloatField()
    description = models.CharField(max_length=255)
    related_fee = models.ForeignKey(
        "Fee", on_delete=models.CASCADE, null=True, blank=True
    )


Account.add_to_class(
    "calculate_balance",
    lambda self: Payment.objects.filter(user=self).aggregate(models.Sum("amount"))[
        "amount__sum"
    ]
    or 0,
)
