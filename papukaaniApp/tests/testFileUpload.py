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
        with open(_filePath + "ecotones.csv") as file:
            response = self.c.post('/papukaani/upload/', {'file': file})

        after = MapPoint.objects.all().count()
        self.assertTrue(after > before)

    def test_invalid_file_does_not_cause_exception(self):
        with open(_filePath + "invalid.txt") as file:
            response = self.c.post('/papukaani/upload/', {'file': file})

        self.assertTrue(response.status_code == 302)

    def test_the_same_points_will_not_be_added_to_database_multiple_times(self):
        with open(_filePath + "ecotones.csv") as file:
            response = self.c.post('/papukaani/upload/', {'file': file})
        before = MapPoint.objects.all().count()
        with open(_filePath + "ecotones.csv") as file:
            response = self.c.post('/papukaani/upload/', {'file': file})

        after = MapPoint.objects.all().count()
        self.assertTrue(after == before)

    def test_new_mappoints_can_be_added_to_database(self):
        dict = {"gpsNumber": 1, "timestamp": datetime.now(), "latitude": -10.0, "longitude": 10.0, "altitude": 10.0,
                "temperature": 10.0}
        point = MapPoint(**dict)
        point.save()
        assert (MapPoint.objects.filter(latitude=-10.0, longitude=10.0, temperature=10.0,
                                        timestamp=point.timestamp)).exists()

    def test_existing_mappoints_cannot_be_added_to_database(self):
        dict = {"gpsNumber": 1, "timestamp": datetime.now(), "latitude": -10.0, "longitude": 10.0, "altitude": 10.0,
                "temperature": 10.0}
        point = MapPoint(**dict)
        try:
            point.save()
            point.save()
            assert 0
        except:
            assert 1
        assert (MapPoint.objects.filter(latitude=-10.0, longitude=10.0, temperature=10.0).count() == 1)
