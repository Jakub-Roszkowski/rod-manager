from django.db import models

from rodManager.dir_models.account import Account, AccountNameSerializer
from rest_framework import serializers

class PlotStatus(models.TextChoices):
    AVAILABLE = "dostepna"
    UNAVAILABLE = "niedostepna"


class Garden(models.Model):
    id = models.AutoField(primary_key=True)
    sector = models.CharField(max_length=255, null=True, blank=True)
    avenue = models.CharField(max_length=255, null=True, blank=True)
    number = models.IntegerField()
    area = models.FloatField(null=True, blank=True)
    leaseholderID = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=PlotStatus.choices,
        default=PlotStatus.AVAILABLE,
    )
    last_leaseholder = models.ForeignKey(Account, on_delete=models.DO_NOTHING, null=True, blank=True, related_name="last_leaseholder")

class GardenNameSerializer(serializers.ModelSerializer):
    leaseholderID = AccountNameSerializer()
    last_leaseholder = AccountNameSerializer()
    class Meta:
        model = Garden
        fields = "__all__"

class GardenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Garden
        exclude = ["leaseholderID", "last_leaseholder"]
        
        
    