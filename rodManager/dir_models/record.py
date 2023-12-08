from django.db import models
from rest_framework import serializers

class Record(models.Model):
    id = models.AutoField(primary_key=True)
    meter = models.ForeignKey("Meter", on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    value = models.FloatField()

class RecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Record
        fields = "__all__"