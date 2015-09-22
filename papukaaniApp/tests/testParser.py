from papukaaniApp.utils.parser import ecotones_parse
from django.test import TestCase
from django.conf import settings
from papukaaniApp.models import Creature, MapPoint


class FileParserTest(TestCase):
    def test_file_parsing(self):
        path = settings.OTHER_ROOT + "/Ecotones_gps_pos_test.csv"
        file = open(path, "rb")
        entries = ecotones_parse(file)
        lats = [61.757366, 61.757366, 61.758000, 61.757200, 61.758050]
        i = 0
        for entry in entries:
            assert float(lats[i]) == float(entry["Latitude"])
            assert float(lats[i]) == float(entry["Latitude"])
            i += 1

    def test_points_can_be_succesfully_created_from_parsed_contents(self):
        path = settings.OTHER_ROOT + "/Ecotones_gps_pos_test.csv"
        file = open(path, "rb")
        entries = ecotones_parse(file)
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
