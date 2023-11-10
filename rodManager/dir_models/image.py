from django.db import models


class Image(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to="images/", null=True, blank=True)
