from django.db import models


class GardenOffers(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    body = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    images = models.ManyToManyField("Image", blank=True)
    contact = models.ForeignKey("Account", null=True, on_delete=models.CASCADE)
    garden = models.ForeignKey(
        "Garden", on_delete=models.CASCADE, blank=True, null=True
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    predicted_rent = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
