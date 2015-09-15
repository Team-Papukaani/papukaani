from django.test import TestCase
from django.test import Client
from papukaaniApp.models import MapPoint
from unittest import mock
from datetime import datetime

class FileUploadTest(TestCase):
    def setUp(self):
        self.c = Client()

    def test_get_to_index_returns_200(self):
        response = self.c.get('/papukaani/')
        self.assertTrue(response.status_code == 200)

    def test_post_to_upload_is_redirected(self):
        response = self.c.get('/papukaani/upload/')
        self.assertTrue(response.status_code == 302)

    def test_post_to_upload_with_file_creates_database_entry(self):
        before = MapPoint.objects.all().count()

        with open("ecotones.csv") as file:
            response = self.c.post('/papukaani/upload/', {'file' : file})

        after = MapPoint.objects.all().count()
        self.assertTrue(after > before)

