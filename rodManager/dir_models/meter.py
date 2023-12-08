from django.db import models
from rest_framework import serializers
from rodManager.dir_models.garden import GardenSerializer


class Meter(models.Model):
    serial = models.CharField(max_length=200, primary_key=True)
    type = models.CharField(max_length=200)
    adress = models.CharField(max_length=200)
    garden = models.ForeignKey()



class MeterSerializer(serializers.ModelSerializer):
    garden = GardenSerializer()
    class Meta:
        model = Meter
        fields = '__all__'