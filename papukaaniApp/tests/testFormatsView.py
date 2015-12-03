from django.test import TestCase, Client
from papukaaniApp.models import GeneralParser
import time

class TestFormatsView(TestCase):

    def setUp(self):
        self.c = Client()
        self.url = "/papukaani/formats/"


    def test_post_to_formats_creates_a_GeneralParser(self):
        response = self.c.post(self.url, data={
            "formatName":"testParser",
            "gpsNumber":"testNumber",
            "timestamp" : "testTime",
            "latitude": "latitude",
            "longitude" : "longitude",
            "delimiter" : ","
        })

        self.assertEquals(len(GeneralParser.objects.all()), 1)

