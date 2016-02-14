from django.test import TestCase
from papukaaniApp.services.deviceindividual_service import DeviceIndividual
from papukaaniApp.models_LajiStore import individual, device


class testLajiStoreAPI(TestCase):
    def setUp(self):
        self.D = device.create(**{
            "deviceManufacturerID": "ABCD1234567",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "dateCreated": "2015-09-29T14:00:00+03:00",
            "dateEdited": "2015-09-29T14:00:00+03:00"
        })

        self.I = individual.create("Lintu1", "test")

    def tearDown(self):
        self.D.delete()
        self.I.delete()
        DeviceIndividual.delete_all()

    def testNoAttachments(self):
        self.assertEquals(0, len(DeviceIndividual.find()))

    def testDeleteAllWorks(self):
        DeviceIndividual.attach(self.D.id, self.I.id, "2015-09-29T14:00:00+03:00")
        self.assertEquals(1, len(DeviceIndividual.find()))
        DeviceIndividual.delete_all()
        self.assertEquals(0, len(DeviceIndividual.find()))

    def testAttachOne(self):
        self.assertEquals(0, len(DeviceIndividual.find()))
        DeviceIndividual.attach(self.D.id, self.I.id, "2015-09-29T14:00:00+03:00")
        self.assertEquals(1, len(DeviceIndividual.find()))

    def testAttach(self):
        self.assertEquals(0, len(DeviceIndividual.find()))
        DeviceIndividual.attach(self.D.id, self.I.id, "2015-09-29T14:00:00+03:00")
        self.assertEquals(1, len(DeviceIndividual.find()))
