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
            assert float(lats[i]) == float(entry["latitude"])
            i += 1

    def test_points_can_be_succesfully_created_from_parsed_contents(self):
        path = settings.OTHER_ROOT + "/Ecotones_gps_pos_test.csv"
        file = open(path, "rb")
        entries = prepare_file(file, "ecotone")
        points = []
        for entry in entries:
            creature, was_created = Creature.objects.get_or_create(name="Pekka")
            point = MapPoint(creature=creature,
                             gpsNumber=entry['gpsNumber'],
                             timestamp=entry['gpsTime'],
                             latitude=entry['latitude'],
                             longitude=entry['longitude'],
                             altitude=entry['altitude'] if entry['altitude'] != '' else 0,
                             temperature=entry['temperature'])
            points.append(point)
        assert len(points) == 5

    def test_byholm_file_parsing(self):
        path = settings.OTHER_ROOT + "/byholm_test.txt"
        file = open(path, "rb")
        entries = prepare_file(file, "byholm")
        lats = [62.86704, 62.86670, 62.86648, 62.86658, 62.86647    ]
        i = 0
        for entry in entries:
            assert float(lats[i]) == float(entry["latitude"])
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
                             timestamp=entry['gpsTime'],
                             latitude=entry['latitude'],
                             longitude=entry['longitude'],
                             altitude=entry['altitude'] if entry['altitude'] != '' else 0,
                             temperature="0")
            points.append(point)
        assert len(points) == 5


