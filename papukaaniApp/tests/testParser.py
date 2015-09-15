from papukaaniApp.utils.parser import ecotones_parse
from django.test import TestCase
from django.conf import settings

class FileParserTest(TestCase):
    def test_file_parsing(self):
        path = settings.OTHER_ROOT + "/Ecotones_gps_pos_test.csv"
        file = open(path)
        entries = ecotones_parse(file)
        lats = [61.757366, 61.757366, 61.758000, 61.757200, 61.758050]
        i = 0
        for entry in entries:
            assert str(lats[i]) in str(entry["latitude"])
            i += 1
