from django.test import TestCase
from django.test import Client
from papukaaniApp.models_LajiStore import document, gathering, device
from papukaaniApp.models import *
from datetime import datetime
import json

_URL = '/papukaani/devices/'


class TestDevice(TestCase):
    def setUp(self):
        self.c = Client()
        self.A = device.create('1234TEST_A','type','manufact','2015-10-27T16:32:01+00:00', '2015-10-27T16:32:01+00:00', [])
        self.B = device.create("1234TEST_B","type","manufact","2015-10-27T16:32:01+00:00", "2015-10-27T16:32:01+00:00", [])

    def tearDown(self):
        self.A.delete()
        self.B.delete()


    def test_devices_are_listed(self):
        response = self.c.get(_URL)
        self.assertTrue("1234TEST_A" in str(response.content))
        self.assertTrue("1234TEST_B" in str(response.content))
