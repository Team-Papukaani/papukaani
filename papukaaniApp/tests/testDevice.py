from django.test import TestCase
from django.test import Client
from papukaaniApp.models_LajiStore import document, gathering, device, individual
from papukaaniApp.models import *
from datetime import datetime
import json

_URL = '/papukaani/devices/'


class TestDevice(TestCase):
    def setUp(self):
        self.c = Client()
        self.A = device.create('1234TEST_A','type','manufact','2015-10-27T16:32:01+00:00', '2015-10-27T16:32:01+00:00', [])
        self.B = device.create("1234TEST_B","type","manufact","2015-10-27T16:32:01+00:00", "2015-10-27T16:32:01+00:00", [])
        self.indiv = individual.create("Indiv", "Tax")

    def tearDown(self):
        self.A.delete()
        self.B.delete()
        self.indiv.delete()

    def test_devices_are_listed(self):
        response = self.c.get(_URL)
        self.assertTrue("1234TEST_A" in str(response.content))
        self.assertTrue("1234TEST_B" in str(response.content))

    def test_post_to_attach_attaches_individual(self):

        response = self.c.post(_URL + "1234TEST_A/attach/", data={
            "individualId" : "Indiv",
            "timestamp" : "2015-10-10T10:10:10+00:00"
        })

        self.A = device.find(deviceId=self.A.deviceId)[0]

        self.assertEquals(1, len(self.A.individuals))

    def test_post_to_remove_removes_individual(self):
        self.A.attach_to(self.indiv,"2015-10-10T10:10:10+00:00" )

        response = self.c.post(_URL + "1234TEST_A/remove/", data={
            "individualId" : "Indiv",
            "timestamp" : "2015-10-10T10:10:10+00:00"
        })

        self.A = device.find(deviceId=self.A.deviceId)[0]

        self.assertEquals(0, len(self.A.individuals))

