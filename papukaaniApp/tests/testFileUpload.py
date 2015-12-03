from django.test import Client
from django.test import TestCase
from papukaaniApp.views import *

_filePath = "papukaaniApp/tests/test_files/"
_URL = '/papukaani/upload/'


class FileUploadTest(TestCase):

    def setUp(self):
        self.c = Client()
        self.ecotone_parser = GeneralParser.objects.create(formatName="ecotone", gpsNumber="GpsNumber", timestamp="timestamp",
                                              longitude="Longtitude", latitude="Latitude", altitude="Altitude",
                                              temperature="Temperature", delimiter=",")
        self.ecotone_parser.save()

    def tearDown(self):
        self.ecotone_parser.delete()
        files = FileStorage.objects.all()
        for f in files:
            f.file.delete(False)
        files.delete()

    def test_get_to_upload_returns_200(self):
        response = self.c.get(_URL)
        self.assertTrue(response.status_code == 200)

    def test_post_to_upload_with_file_creates_database_entry(self):
        document.delete_all()
        before = len(document.get_all())
        self.submit_file("ecotones.csv")

        after = len(document.get_all())
        self.assertTrue(after > before)

    def test_invalid_file_does_not_cause_exception(self):
        response = self.submit_file("invalid.txt")
        self.assertTrue(response.status_code == 302)

    def test_the_same_points_will_not_be_added_to_database_multiple_times(self):
        self.submit_file("ecotones.csv")
        before = len(document.get_all())
        self.submit_file("ecotones.csv")

        after = len(document.get_all())
        self.assertTrue(after == before)

    def test_file_can_be_found_from_db_after_upload(self):
        FileStorage.objects.all().delete()
        self.submit_file("ecotones.csv")
        files = FileStorage.objects.all()
        self.assertEquals(1, len(files))

    def submit_file(self, filename):
        with open(_filePath + filename) as file:
            return self.c.post('/papukaani/upload/', {'file': file, 'fileFormat': "ecotone"})


