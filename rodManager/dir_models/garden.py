from django.db import models


class PlotStatus(models.TextChoices):
    AVAILABLE = "dostępna", _("Available")
    UNAVAILABLE = "niedostępna", _("Unavailable")


class Garden(models.Model):
    id = models.CharField(max_length=255, primary_key=True)
    sector = models.CharField(max_length=255, null=True, blank=True)
    avenue = models.CharField(max_length=255, null=True, blank=True)
    number = models.IntegerField()
    area = models.FloatField(null=True, blank=True)
    leaseholderID = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=PlotStatus.choices,
        default=PlotStatus.AVAILABLE,
    )
