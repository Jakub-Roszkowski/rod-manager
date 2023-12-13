from django.db import models


class RODGardens(models.Model):
    RODDescription = models.TextField(blank=True, null=True)