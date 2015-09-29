from django.test import TestCase
from django.test import Client
from papukaaniApp.models import *
from datetime import datetime

_URL = '/papukaani/choose/'


class TestChoose(TestCase):
    def setUp(self):
        self.c = Client()
        self.creature = Creature.objects.create(name="Creature")
        self.A = MapPoint.objects.create(
            creature=self.creature,
            gpsNumber=1,
            latitude=22.22,
            longitude=22.22,
            altitude=222.22,
            temperature=22.2,
            timestamp=datetime.now(),
        )
        self.B = MapPoint.objects.create(
            creature=self.creature,
            gpsNumber=2,
            latitude=11.22,
            longitude=11.22,
            altitude=111.22,
            temperature=11.2,
            timestamp=datetime.now()
        )

    def test_post_with_data_changes_database_entries(self):
        Aid = self.A.id
        Bid = self.B.id
        response = self.c.post(_URL, {
            'data': '[{"id" : ' + str(Aid) + ', "public" : true},{"id" : ' + str(Bid) + ', "public" : false}]'})

        self.A = MapPoint.objects.get(id=Aid)
        self.B = MapPoint.objects.get(id=Bid)

        self.assertTrue(self.A.public)
        self.assertFalse(self.B.public)

    def test_get_returns_200(self):
        response = self.c.get(_URL)
        self.assertTrue(response.status_code == 200)


    def test_post_without_data_is_redirected(self):
        response = self.c.post(_URL)
        self.assertTrue(response.status_code == 302)

    def test_get_returns_points(self):
        response = self.c.get(_URL)
        self.assertTrue("[{" in str(response.content))
        self.assertTrue("latlong" in str(response.content))
        self.assertTrue("id" in str(response.content))
