from papukaaniApp.tests import test_data
from papukaaniApp.utils.file_preparer import _check_that_file_is_valid
from papukaaniApp.utils.parser import *
from django.test import TestCase
from django.conf import settings
from papukaaniApp.models import *
from papukaaniApp.models_LajiStore import document
from papukaaniApp.tests.test_data import create_jouko_parser


class FilePreparerTest(TestCase):
    def setUp(self):
        self.ecotone_parser = GeneralParser.objects.create(formatName="ecotone", manufacturerID="GpsNumber",
                                                           timestamp="GPSTime",
                                                           longitude="Longtitude", latitude="Latitude",
                                                           altitude="Altitude",
                                                           temperature="Temperature")
        self.ecotone_parser.save()

        self.byholm_parser = GeneralParser.objects.create(formatName="byholm", timestamp="DateTime",
                                                          longitude="Longitude_E", latitude="Latitude_N",
                                                          altitude="Altitude_m",
                                                          temperature="temperature")
        self.byholm_parser.save()

    def tearDown(self):
        document.delete_all()

        self.ecotone_parser.delete()
        self.byholm_parser.delete()

    def test_byholm_file_parsing(self):
        path = settings.OTHER_ROOT + "/byholm_test.txt"
        file = open(path, "rb")
        entries = prepare_file(file, self.byholm_parser, "1010")
        lats = [62.86704, 62.86670, 62.86648, 62.86658, 62.86647]
        i = 0
        for entry in entries:
            assert float(lats[i]) == float(entry["latitude"])
            i += 1
        assert len(entries) == 5

    def test_file_with_separate_time_and_date_is_correct(self):
        _check_that_file_is_valid(open('papukaaniApp/tests/test_files/Jouko.txt').readlines(), test_data.create_jouko_parser()) #Raises exception if not valid

    def test_file_with_missing_headers_is_not_correct(self):
        with self.assertRaises(AssertionError):
            _check_that_file_is_valid(open('papukaaniApp/tests/test_files/Jouko_invalid.txt').readlines(), test_data.create_jouko_parser())

    def test_file_parsing(self):
        path = settings.OTHER_ROOT + "/Ecotones_gps_pos_test.csv"
        file = open(path, "rb")
        entries = prepare_file(file, self.ecotone_parser)
        lats = [61.757366, 61.757366, 61.758000, 61.757200, 61.758050]
        i = 0
        for entry in entries:
            assert float(lats[i]) == float(entry["latitude"])
            assert float(lats[i]) == float(entry["latitude"])
            i += 1
        assert len(entries) == 5
