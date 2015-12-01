from django.db import models
from django.db.models.signals import pre_init


class Creature(models.Model):
    name = models.CharField(max_length=300)

    def return_public_points(self):
        """
        This method returns public points from the database.

        :return: MapPoint objects that contains public points
        """
        return MapPoint.objects.filter(creature=self).filter(public=True)

class FileStorage(models.Model):
    file = models.FileField()
    name = models.CharField(max_length=40, blank=True)
    uploadTime = models.DateTimeField(blank=True)

class MapPoint(models.Model):
    creature = models.ForeignKey(Creature)
    gpsNumber = models.CharField(max_length=20)
    timestamp = models.DateTimeField()
    latitude = models.DecimalField(max_digits=12, decimal_places=9)  # decimals are important, float approximates
    longitude = models.DecimalField(max_digits=12, decimal_places=9)
    altitude = models.DecimalField(max_digits=8, decimal_places=3)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    public = models.BooleanField(default=False)

    class Meta:
        unique_together = ("gpsNumber", "timestamp", "latitude", "longitude")


class GeneralParser(models.Model):
    formatName = models.CharField(max_length=50)
    gpsNumber = models.CharField(max_length=50, blank=True)
    gpsTime = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    altitude = models.CharField(max_length=50, blank=True)
    temperature = models.CharField(max_length=50, blank=True)
    delimiter = models.CharField(max_length=50)
