from datetime import datetime
from django.db import models
from django.db.models.signals import pre_init
from django.test import TestCase

from papukaaniApp.models import Creature
from papukaaniApp.models import MapPoint


class return_public_point_test(TestCase):

    def test_return_public_point(self):
        creat = Creature.objects.create(name='creature1')

        for x in range(0, 100):
            MapPoint.objects.create(creature = creat,
                                       timestamp = datetime.now(),
                                       latitude = 111.111111111,
                                       longitude = 222.222222222,
                                       altitude = 33333.333,
                                       temperature = x,
                                       public=x%2==0)


        mappR = creat.return_public_points()
        self.assertTrue(mappR.count()==50)





