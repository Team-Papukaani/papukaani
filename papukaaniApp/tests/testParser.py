from papukaaniApp.utils.parser import *
from django.test import TestCase
from django.conf import settings
from papukaaniApp.models import Creature, MapPoint
from papukaaniApp.models_LajiStore import document, gathering


class FileParserTest(TestCase):
    def tearDown(self):
        document.delete_all()

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

    def test_create_points_method_correctly_updates_existing_documents(self):
        _create_points_from_ecotone("/Ecotones_gps_pos_doc_create_test.csv")
        _create_points_from_ecotone("/Ecotones_gps_pos_doc_create_test2.csv")
        assert len(document.get_all()) == 3

    def test_merge_and_delete_if_three_documents_found_for_same_device(self):

        gatherings = [gathering.Gathering("2015-09-15T08:00:00+03:00", [68.93023632, 23.19298104])]
        dict = {
            "documentId": "TestId0000001",
            "deviceId" : "48500691564",
            "createdAt":"2015-09-14T15:29:28+03:00",
            "lastModifiedAt":"2015-09-14T15:29:28+03:00",
            "facts": [],
            "gatherings": gatherings
            }
        document.create(**dict)
        document.create(**dict)
        document.create(**dict)
        assert len(document.get_all()) == 3

        _create_points_from_ecotone("/Ecotones_gps_pos_test.csv")
        assert len(document.get_all()) == 1


def _create_points_from_ecotone(filename):
        path = settings.OTHER_ROOT + filename
        file = open(path, "rb")
        entries = ecotones_parse(file)
        create_points(entries)
