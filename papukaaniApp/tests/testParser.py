from papukaaniApp.utils.parser import *
from django.test import TestCase
from django.conf import settings
from papukaaniApp.models_LajiStore import document, gathering
from papukaaniApp.models import *
from random import *
import time
from papukaaniApp.utils.parser import _extract_timestamp


class FileParserTest(TestCase):
    def setUp(self):
        self.ecotone_parser = GeneralParser.objects.create(formatName="ecotone", gpsNumber="GpsNumber",
                                                           timestamp="GPSTime",
                                                           longitude="Longtitude", latitude="Latitude",
                                                           altitude="Altitude",
                                                           temperature="Temperature", delimiter=",")


        self.ecotone_parser.save()

        self.byholm_parser = GeneralParser.objects.create(formatName="byholm", timestamp="DateTime",
                                                          longitude="Longitude_E", latitude="Latitude_N",
                                                          altitude="Altitude_m",
                                                          temperature="temperature", delimiter="\t")
        self.byholm_parser.save()


    def tearDown(self):
        document.delete_all()

        self.ecotone_parser.delete()
        self.byholm_parser.delete()

    def test_create_points_method_correctly_updates_existing_documents(self):
        _create_points_from_ecotone(self, "/Ecotones_gps_pos_doc_create_test.csv")
        _create_points_from_ecotone(self, "/Ecotones_gps_pos_doc_create_test2.csv")
        assert len(document.get_all()) == 3

    def test_merge_and_delete_if_three_documents_found_for_same_device(self):
        gatherings = [gathering.Gathering("2015-09-15T08:00:00+03:00", [68.93023632, 23.19298104])]
        dict = {
            "documentId": "TestId0000001",
            "deviceId": "48500691564",
            "createdAt": "2015-09-14T15:29:28+03:00",
            "lastModifiedAt": "2015-09-14T15:29:28+03:00",
            "facts": [],
            "gatherings": gatherings
        }
        document.create(**dict)
        document.create(**dict)
        document.create(**dict)
        assert len(document.get_all()) == 3

        _create_points_from_ecotone(self, "/Ecotones_gps_pos_test.csv")
        assert len(document.get_all()) == 1

    def test_document_does_not_contain_duplicate_gathering(self):
        _create_points_from_ecotone(self, "/Ecotones_gps_pos_gathering_duplicate_test.csv")
        _create_points_from_ecotone(self, "/Ecotones_gps_pos_gathering_duplicate_test2.csv")
        documents = document.get_all()
        self.assertEqual(len(documents[0].gatherings), 1)

    def test_gathering_facts_unite_succesfully(self):
        document.delete_all()
        _create_points_from_ecotone(self, "/Ecotones_gps_pos_gathering_duplicate_test.csv", "01-01-1000, 00-00-00")
        _create_points_from_ecotone(self, "/Ecotones_gps_pos_gathering_duplicate_test.csv", "24-11-2015, 00-00-00")
        documents = document.get_all()
        self.assertEquals(6, len(documents[0].gatherings[0].facts))
        facts = documents[0].gatherings[0].facts
        self.assertEquals(facts[1]["value"], "24-11-2015, 00-00-00")
        self.assertEquals(facts[4]["value"], "01-01-1000, 00-00-00")

    def test_byholm_data_goes_to_lajiStore_succesfully(self):
        document.delete_all()
        path = settings.OTHER_ROOT + "/byholm_test.txt"
        file = open(path, "rb")
        entries = prepare_file(file, self.byholm_parser, "1010")
        create_points(entries, self.byholm_parser, "byholm_test.txt",
                      datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
        documents = document.get_all()
        self.assertEqual(len(documents), 1)
        self.assertEqual(len(documents[0].gatherings), 5)

    def test_generating_timestamp_works_with_separate_date_and_time(self):
        self.assertEqual(_extract_timestamp({'date': '12-10-2014', 'time': '10:01'}), '2014-10-12T10:01:00+00:00')

    def test_generating_timestamp_works_with_date_and_time_together(self):
        self.assertEqual(_extract_timestamp({'timestamp': '12-10-2014 10:01'}), '2014-10-12T10:01:00+00:00')


    def test_filename_and_datetime_goes_to_facts(self):
        _create_points_from_ecotone(self, "/Ecotones_gps_pos_doc_create_test.csv")
        documents = document.get_all()
        self.assertEqual(len(documents[0].gatherings[0].facts), 3)

    def test_altitude_in_facts(self):
        _create_points_from_ecotone(self, "/Ecotones_gps_pos_doc_create_test.csv")
        time.sleep(3)
        documents = document.get_all()
        result = False
        facts = documents[0].gatherings[0].facts
        for fact in facts:
            if fact["name"] == "altitude":
                if fact["value"] == "1":
                    result = True
        self.assertEquals(result, True)


def _create_points_from_ecotone(self, filename, time=datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S")):
    path = settings.OTHER_ROOT + filename
    file = open(path, "rb")
    entries = prepare_file(file, self.ecotone_parser)
    create_points(entries, self.ecotone_parser, filename, time)
