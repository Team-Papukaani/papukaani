from django.db import models
from django.db.models.signals import pre_init

class FileStorage(models.Model):
    file = models.FileField()
    filename = models.CharField(max_length=40, blank=True)
    uploadTime = models.DateTimeField(blank=True)

class GeneralParser(models.Model):
    formatName = models.CharField(max_length=50)
    gpsNumber = models.CharField(max_length=50, blank=True)
    gpsTime = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    altitude = models.CharField(max_length=50, blank=True)
    temperature = models.CharField(max_length=50, blank=True)
    delimiter = models.CharField(max_length=50)
