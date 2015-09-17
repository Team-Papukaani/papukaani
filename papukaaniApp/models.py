from django.db import models


class Creature(models.Model):
    name = models.CharField(max_length=300)
    gpsNumber = models.IntegerField()  # gpsNumber integer or varchar?


class MapPoint(models.Model):
    creature = models.ForeignKey(Creature, primary_key=True)
    timestamp = models.DateTimeField(primary_key=True)
    latitude = models.DecimalField(max_digits=12, decimal_places=9)  # decimals are important, float approximates
    longitude = models.DecimalField(max_digits=12, decimal_places=9)
    altitude = models.DecimalField(max_digits=8, decimal_places=3)
    temperature = models.DecimalField(max_digits=5, decimal_places=2)

    def __init__(self, **point):
        self.creature = Creature.objects.get_or_create(gpsNumber=point["gpsNumber"], defaults={'name': 'TEMPORARY'})
        point.pop('gpsNumber')
        super(MapPoint, self).__init__(**point)