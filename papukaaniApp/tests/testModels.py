from datetime import datetime
from django.test import TestCase

from papukaaniApp.models import Creature
from papukaaniApp.models import MapPoint


class ReturnPublicPointsTest(TestCase):

    def test_return_public_points(self):
        creat = Creature.objects.create(name='creature1')
        for x in range(0, 3):
            MapPoint.objects.create(creature = creat,
                                       gpsNumber = x,
                                       timestamp = datetime.now(),
                                       latitude = 111.111111111,
                                       longitude = 222.222222222,
                                       altitude = 33333.333,
                                       temperature = 12,
                                       public=x%2==0)

        mappR = creat.return_public_points()
        self.assertTrue(mappR.count()==2)





