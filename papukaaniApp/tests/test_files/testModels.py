from django.test import TestCase
from django.conf import settings
from papukaaniApp.models import Creature

class return_public_points_test():
    def test_file_parsing(self):
        creature =      "/luo testi creature/"
        creature.name = "test"
        creature.gpsNumber = 100
        points = creature.return_public_points()
        "/testaa points not empty tms./"