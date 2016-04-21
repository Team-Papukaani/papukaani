from urllib.parse import urlencode
from django.test import TestCase
from django.test import Client
from papukaaniApp.services.deviceindividual_service import DeviceIndividual
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

    def test_attaches(self):

        response = self.c.post(_URL + "attachments/", data={
            "deviceID": self.A.id,
            "individualID": self.indiv.id,
            "attached": "2015-10-10T10:10:10+00:00"
        })

        self.assertNotEquals(None, self.A.get_attached_individualid())

    def test_removes(self):
        self.A.attach_to(self.indiv.id, "2015-10-10T10:10:10+00:00" )
        attID = DeviceIndividual.get_active_attachment_of_device(self.A.id)['id']

        # https://github.com/jgorset/django-respite/issues/38
        response = self.c.put(
            path=_URL + "attachments/" + attID, 
            data=urlencode({
                "id": attID,
                "individualID" : self.indiv.id,
                "deviceID" : self.A.id,
                "attached" : "2015-10-10T10:10:10+00:00",
                "removed" :  "2015-10-10T10:10:11+00:00"
            }), 
            content_type='application/x-www-form-urlencoded')

        self.assertEquals(None, self.A.get_attached_individualid())

