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
        to="Garden", on_delete=models.DO_NOTHING, null=True, blank=True
    )

    def calculate_usage(self, calculation_date, previous_calculation_date=None):
        try:
            previous_record = Record.objects.filter(
                meter=self, datetime__lte=previous_calculation_date
            ).order_by("-datetime")[0]
        except:
            try:
                previous_record = Record.objects.filter(
                    meter=self, datetime__lte=calculation_date
                ).order_by("datetime")[0]
            except:
                previous_record = None

        try:
            current_record = Record.objects.filter(
                meter=self, datetime__lte=calculation_date
            ).order_by("-datetime")[0]
        except:
            current_record = None

        if previous_record and current_record:
            return current_record.value - previous_record.value
        else:
            return 0


class MeterSerializer(serializers.ModelSerializer):
    garden = GardenSerializer()

    class Meta:
        model = Meter
        fields = "__all__"


class MeterLastRecordSerializer(serializers.ModelSerializer):
    value = serializers.SerializerMethodField()

    def get_value(self, obj):
        return (
            Record.objects.filter(meter=obj).order_by("-datetime")[0].value
            if Record.objects.filter(meter=obj).exists()
            else None
        )

    class Meta:
        model = Meter
        fields = "__all__"
