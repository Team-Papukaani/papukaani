from django.test import TestCase
from django.test import Client
from papukaaniApp.models_LajiStore import device, individual

_URL = '/papukaani/devices/'


class TestDevice(TestCase):
    def setUp(self):
        self.c = Client()
        self.A = device.create("type","Manufacturer1",'1234TEST_A',"2015-10-27T16:32:01+00:00", "2015-10-27T16:32:01+00:00")
        self.B = device.create("type","Manufacturer2","1234TEST_B","2015-10-27T16:32:01+00:00", "2015-10-27T16:32:01+00:00")
        self.indiv = individual.create("Lintu1","Tax")

    def tearDown(self):
        self.A.delete()
        self.B.delete()
        self.indiv.delete()

    def test_devices_are_listed(self):
        response = self.c.get(_URL)
        self.assertTrue("1234TEST_A" in str(response.content))
        self.assertTrue("1234TEST_B" in str(response.content))

    def test_post_to_attach_attaches_individual(self):

        response = self.c.post(_URL + self.A.id + "/attach/", data={
            "individualId": self.indiv.id,
            "timestamp": "2015-10-10T10:10:10+00:00"
        })

        self.assertNotEquals(None, self.A.get_attached_individualid())

    def test_post_to_remove_removes_individual(self):
        self.A.attach_to(self.indiv.id, "2015-10-10T10:10:10+00:00" )

        response = self.c.post(_URL + self.A.id + "/remove/", data={
            "individualId" : self.indiv.id,
            "timestamp" : "2015-10-10T10:10:10+00:00"
        })

        self.assertEquals(None, self.A.get_attached_individualid())

