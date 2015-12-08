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


    def test_post_to_formats_creates_a_GeneralParser(self):
        response = self.c.post(self.url, data={
            "formatName":"testParser",
            "gpsNumber":"testNumber",
            "gpsTime" : "testTime",
            "latitude": "latitude",
            "longitude" : "longitude",
            "delimiter" : ","
        })
        
        self.assertEquals(len(GeneralParser.objects.all()), 1)

