from django.test import Client
from django.test import TestCase
from django.conf import settings
from papukaaniApp.models import *
from papukaaniApp.models_LajiStore import *
from papukaaniApp.views import *

_filePath = "papukaaniApp/tests/test_files/"
_URL = '/papukaani/upload/'


class FileUploadTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.ecotone_parser = GeneralParser.objects.create(formatName="ecotone", gpsNumber="GpsNumber", gpsTime="GPSTime",
                                              longitude="Longtitude", latitude="Latitude", altitude="Altitude",
                                              temperature="Temperature", delimiter=",")
        self.ecotone_parser.save()

    def tearDown(self):
        self.ecotone_parser.delete()


    def test_get_to_upload_returns_200(self):
        response = self.c.get(_URL)
        self.assertTrue(response.status_code == 200)

    def test_post_to_upload_with_file_creates_database_entry(self):
        before = len(document.get_all())
        self.submit_file("ecotones.csv", "ecotone")

        after = len(document.get_all())
        self.assertTrue(after > before)

    def test_invalid_file_does_not_cause_exception(self):
        response = self.submit_file("invalid.txt", "ecotone")

        self.assertTrue(response.status_code == 302)

    def test_the_same_points_will_not_be_added_to_database_multiple_times(self):
        self.submit_file("ecotones.csv", "ecotone")
        before = len(document.get_all())
        self.submit_file("ecotones.csv", "ecotone")

        after = len(document.get_all())
        self.assertTrue(after == before)

    def test_file_can_be_found_from_db_after_upload(self):
        self.submit_file("ecotones.csv", "ecotone")
        files = FileStorage.objects.get()
        self.assertEquals(1, len(files))
        self.assertEquals("test", files[0])

    def submit_file(self, filename, formatname):
        with open(_filePath + filename) as file:
            return self.c.post('/papukaani/upload/', {'file': file, 'fileFormat': formatname})


