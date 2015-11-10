from papukaaniApp.utils.parser import *
from django.test import TestCase
from django.conf import settings
from papukaaniApp.models import Creature, MapPoint
from papukaaniApp.models_LajiStore import document, gathering

class FilePreparerTest(TestCase):
    def tearDown(self):
        document.delete_all()

    def test_file_parsing(self):
        path = settings.OTHER_ROOT + "/Ecotones_gps_pos_test.csv"
        file = open(path, "rb")
        entries = prepare_file(file, "ecotone")
        lats = [61.757366, 61.757366, 61.758000, 61.757200, 61.758050]
        i = 0
        for entry in entries:
            assert float(lats[i]) == float(entry["Latitude"])
            assert float(lats[i]) == float(entry["Latitude"])
            i += 1

    def test_points_can_be_succesfully_created_from_parsed_contents(self):
        path = settings.OTHER_ROOT + "/Ecotones_gps_pos_test.csv"
        file = open(path, "rb")
        entries = prepare_file(file, "ecotone")
        points = []
        for entry in entries:
            creature, was_created = Creature.objects.get_or_create(name="Pekka")
            point = MapPoint(creature=creature,
                             gpsNumber=entry['GpsNumber'],
                             timestamp=entry['GPSTime'],
                             latitude=entry['Latitude'],
                             longitude=entry['Longtitude'],
                             altitude=entry['Altitude'] if entry['Altitude'] != '' else 0,
                             temperature=entry['Temperature'])
            points.append(point)
        assert len(points) == 5

    def test_byholm_file_parsing(self):
        path = settings.OTHER_ROOT + "/byholm_test.txt"
        file = open(path, "rb")
        entries = prepare_file(file, "byholm")
        lats = [62.86704, 62.86670, 62.86648, 62.86658, 62.86647    ]
        i = 0
        for entry in entries:
            assert float(lats[i]) == float(entry["Latitude_N"])
            assert float(lats[i]) == float(entry["Latitude_N"])
            i += 1

    def test_byholm_points_can_be_succesfully_created_from_parsed_contents(self):
        path = settings.OTHER_ROOT + "/byholm_test.txt"
        file = open(path, "rb")
        entries = prepare_file(file, "byholm")
        points = []
        for entry in entries:
            creature, was_created = Creature.objects.get_or_create(name="Pekka")
            point = MapPoint(creature=creature,
                             gpsNumber="0",
                             timestamp=entry['DateTime'],
                             latitude=entry['Latitude_N'],
                             longitude=entry['Longitude_E'],
                             altitude=entry['Altitude_m'] if entry['Altitude_m'] != '' else 0,
                             temperature="0")
            points.append(point)
        assert len(points) == 5


