from django.test import TestCase
from django.test import Client
from papukaaniApp.models import MapPoint
from unittest import mock
from datetime import datetime

_filePath = "papukaaniApp/tests/test_files/"

class FileUploadTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_get_to_upload_returns_200(self):
        response = self.c.get('/papukaani/upload/')
        self.assertTrue(response.status_code == 200)

    def test_post_to_upload_is_redirected(self):
        response = self.c.get('/papukaani/upload/')

        self.assertTrue(response.status_code == 200)

    def test_post_to_upload_with_file_creates_database_entry(self):
        before = MapPoint.objects.all().count()

        with open(_filePath+"ecotones.csv") as file:
            response = self.c.post('/papukaani/upload/', {'file' : file})

        after = MapPoint.objects.all().count()
        self.assertTrue(after > before)

    def test_file_upload_response_contains_json(self):
        with open(_filePath + "ecotones.csv") as file:
            response = self.c.post('/papukaani/upload/', {'file' : file})

        self.assertTrue("latitude" in  str(response.content))
        self.assertTrue("[{" in  str(response.content))
        self.assertTrue("longitude" in  str(response.content))

    def test_invalid_file_does_not_cause_exception(self):
        with open(_filePath+"invalid.txt") as file:
            response = self.c.post('/papukaani/upload/', {'file' : file})

        self.assertTrue(response.status_code == 302)

