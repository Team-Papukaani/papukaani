from django.test import TestCase
from django.test import Client
from papukaaniApp import views
from django.conf import settings


class FileUploadTest(TestCase):
    def test_get_to_index_returns_200(self):
        c = Client()
        response = c.get('/papukaani/')
        self.assertTrue(response.status_code == 200)

    def test_post_to_index_returns_200(self):
        c = Client()
        response = c.get('/papukaani/')
        self.assertTrue(response.status_code == 200)


class FileParserTest(TestCase):
    def test_file_parsing(self):
        path = settings.OTHER_ROOT + "/Ecotones_gps_pos_test.csv"
        file = open(path)
        entries = views.ecotones_parse(file)
        lats = [61.757366, 61.757366, 61.758000, 61.757200, 61.758050]
        i = 0
        for entry in entries:
            assert str(lats[i]) in str(entry["latitude"])
            i += 1
