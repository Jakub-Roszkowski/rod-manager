from attr import fields
from django.db import models
from rest_framework import serializers

from rodManager.dir_models.garden import GardenSerializer
from rodManager.dir_models.record import Record


class Meter(models.Model):
    serial = models.CharField(max_length=200, primary_key=True)
    type = models.CharField(max_length=200)
    adress = models.CharField(max_length=200)
    garden = models.ForeignKey(
        to="Garden", on_delete=models.CASCADE, null=True, blank=True
    )


class MeterSerializer(serializers.ModelSerializer):
    garden = GardenSerializer()

    class Meta:
        model = Meter
        fields = "__all__"


class MeterLastRecordSerializer(serializers.ModelSerializer):
    record = serializers.StringRelatedField(many=True)

    class Meta:
        model = Meter
        fields = "__all__"
