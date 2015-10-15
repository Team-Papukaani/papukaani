from django.test import TestCase
from django.test import Client
from papukaaniApp.models_LajiStore import document, gathering
from papukaaniApp.models import *
from datetime import datetime
import json

_URL = '/papukaani/choose/'


class TestChoose(TestCase):
    def setUp(self):
        self.c = Client()
        self.A = document.create("TestA", [gathering.Gathering("1234-12-12T12:12:12+00:00", [22.2, 22.2])], "DeviceId")
        self.B = document.create("TestB", [gathering.Gathering("1234-12-12T12:12:12+00:00", [32.2, 32.2])], "DeviceId")

    def tearDown(self):
        self.A.delete()
        self.B.delete()

    def test_post_with_data_changes_database_entries(self):
        Aid = self.A.id
        Bid = self.B.id

        self.A.gatherings[0].publicity = "public"

        response = self.c.post(_URL, {
            'data': '['+  json.dumps(self.A.to_dict())+','+ json.dumps(self.B.to_dict())+']'})


        self.A = document.get(id=Aid)
        self.B = document.get(id=Bid)

        self.assertEquals(self.A.gatherings[0].publicity, "public")
        self.assertEquals(self.B.gatherings[0].publicity, "private")

    def test_get_returns_200(self):
        response = self.c.get(_URL)
        self.assertTrue(response.status_code == 200)


    def test_post_without_data_is_redirected(self):
        response = self.c.post(_URL)
        self.assertTrue(response.status_code == 302)

    def test_get_returns_points(self):
        response = self.c.get(_URL)
        self.assertTrue("[{" in str(response.content))
        self.assertTrue("id" in str(response.content))
