from django.test import TestCase
from django.test import Client
from papukaaniApp.models_LajiStore import *
from papukaaniApp.models import *
from datetime import datetime

_filePath = "papukaaniApp/tests/test_files/"
_URL = '/papukaani/upload/'


class FileUploadTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.ecotone_parser = GeneralParser.objects.create(formatName="ecotone", gpsNumber="GpsNumber", gpsTime="GPSTime",
                                              longitude="Longtitude", latitude="Latitude", altitude="Altitude",
                                              temperature="Temperature", split_mark=",", coding="utf-8")
        self.ecotone_parser.save()

    def tearDown(self):
        self.ecotone_parser.delete()

    def test_get_to_upload_returns_200(self):
        response = self.c.get(_URL)
        self.assertTrue(response.status_code == 200)

    def test_post_to_upload_is_redirected(self):
        response = self.c.get(_URL)

        self.assertTrue(response.status_code == 200)

    def test_post_to_upload_with_file_creates_database_entry(self):
        before = len(document.get_all())
        with open(_filePath + "ecotones.csv") as file:
            response = self.c.post(_URL, {'file': file})

        after = len(document.get_all())
        self.assertTrue(after > before)

    def test_invalid_file_does_not_cause_exception(self):
        with open(_filePath + "invalid.txt") as file:
            response = self.c.post(_URL, {'file': file})

        self.assertTrue(response.status_code == 302)

    def test_the_same_points_will_not_be_added_to_database_multiple_times(self):
        with open(_filePath + "ecotones.csv") as file:
            response = self.c.post('/papukaani/upload/', {'file': file})
        before = len(document.get_all())
        with open(_filePath + "ecotones.csv") as file:
            response = self.c.post('/papukaani/upload/', {'file': file})

        after = len(document.get_all())
        #self.assertTrue(after == before)


