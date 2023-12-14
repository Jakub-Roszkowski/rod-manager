from django.db import models
from rest_framework import serializers

class RODGardens(models.Model):
    RODDescription = models.TextField(blank=True, null=True)


class RODGardensSerializer(serializers.ModelSerializer):
    class Meta:
        model = RODGardens
        fields = "__all__"