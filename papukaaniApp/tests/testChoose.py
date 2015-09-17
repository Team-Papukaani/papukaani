from django.test import TestCase
from django.test import Client
from papukaaniApp.models import *
from datetime import datetime

class TestChoose(TestCase):

    def setUp(self):
        self.c = Client()
        self. creature = Creature.objects.create(name="Creature", gpsNumber="1")
        self.A = MapPoint.objects.create(
            creature = self.creature,
            gpsNumber = "1",
            latitude = 22.22,
            longitude = 22.22,
            altitude = 222.22,
            temperature = 22.2,
            timestamp = datetime.now()
        )
        self.B = MapPoint.objects.create(
            creature = self.creature,
            gpsNumber = "1",
            latitude = 11.22,
            longitude = 11.22,
            altitude = 111.22,
            temperature = 11.2,
            timestamp = datetime.now()
        )


    def test(self):
        self.assertTrue(True)


