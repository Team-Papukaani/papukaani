from papukaaniApp.utils.parser import *
from django.test import TestCase
from django.conf import settings
from papukaaniApp.models import *
from papukaaniApp.models_LajiStore import document


class FilePreparerTest(TestCase):
    def setUp(self):
        self.ecotone_parser = GeneralParser.objects.create(formatName="ecotone", gpsNumber="GpsNumber",
                                                           gpsTime="GPSTime",
                                                           longitude="Longtitude", latitude="Latitude",
                                                           altitude="Altitude",
                                                           temperature="Temperature", delimiter=",")
        self.ecotone_parser.save()

        self.byholm_parser = GeneralParser.objects.create(formatName="byholm", gpsTime="DateTime",
                                                          longitude="Longitude_E", latitude="Latitude_N",
                                                          altitude="Altitude_m",
                                                          temperature="temperature", delimiter="\t")
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

