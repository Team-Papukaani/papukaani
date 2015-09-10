from django.db import models

class Creature(models.Model):
    name = models.CharField(max_length=300)
    gpsNumber = models.IntegerField(max_length=20)

class MapPoint(models.Model):
    timestamp = models.DateTimeField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9)  # decimals are important, float approximates
    longitude = models.DecimalField(max_digits=12, decimal_places=9)
    altitude = models.DecimalField(max_digits=8, decimal_places=3)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)

