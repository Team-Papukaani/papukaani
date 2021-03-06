from django.test import TestCase, Client
from papukaaniApp.models import GeneralParser
import time
from django.conf import settings

class TestFormatsView(TestCase):

    def setUp(self):
        self.c = Client()
        self.url = "/papukaani/formats/0/"
        GeneralParser.objects.all().delete()
        settings.MOCK_AUTHENTICATION = "Skip"

    def tearDown(self):
        GeneralParser.objects.all().delete()

    def test_post_to_formats_creates_a_GeneralParser(self):
        GeneralParser.objects.all().delete()
        response = self.c.post(self.url, data={
            "formatName":"testParser",
            "manufacturerID":"testNumber",
            "timestamp" : "testTime",
            "latitude": "latitude",
            "longitude" : "longitude",
        })

        self.assertEquals(len(GeneralParser.objects.all()), 1)

    def test_post_uncomplete_info_to_formats_does_not_create_parser(self):
        GeneralParser.objects.all().delete()
        self.c.post(self.url, data={
            "formatName":"",
            "manufacturerID":"testNumber",
            "gpsTime" : "testGPS",
            "latitude": "latitude",
            "longitude" : "longitude",
        })

        self.assertEquals(len(GeneralParser.objects.all()), 0)
