from django.test import TestCase
from papukaaniApp.models_LajiStore import *


class TestDevice(TestCase):
    def setUp(self):
        dev = {
            "deviceManufacturerID": "ABCD1234567",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "dateCreated": "2015-09-29T14:00:00+03:00",
            "dateEdited": "2015-09-29T14:00:00+03:00"
        }

        self.d = device.create(**dev)

    def tearDown(self):
        self.d.delete()

    def test_create_and_delete(self):
        self.assertEquals("ABCD1234567", self.d.deviceId)
        self.assertEquals("Type", self.d.deviceType)
        self.assertEquals("Manufacturer", self.d.deviceManufacturer)

    def test_update_and_get(self):
        self.d.deviceType = "NewType"
        self.d.update()
        gotten = device.get(self.d.id)
        self.assertEquals("NewType", gotten.deviceType)

    def test_get_all(self):
        self.assertGreater(len(device.get_all()), 0)

    def test_get_or_create(self):
        before = len(device.get_all())
        device.get_or_create("ABCD1234567", {"type":"Type", "manufacturer":"Manu"})
        self.assertEquals(before, len(device.get_all()))

        d = device.get_or_create("TESTTEST", {"type":"Type", "manufacturer":"Manu"})
        self.assertLess(before, len(device.get_all()))

        d.delete()

    def test_attach(self):
        A, B = self._create_individuals()
        self.d.attach_to(A, "2015-10-10T10:10:10+00:00")
        self.assertEquals(self.d.individuals[0]["individualId"], A.individualId)
        self._delete_individuals([A, B])

    def test_device_not_attach_if_unremoved_devices_in_individuals(self):
        self.d.individuals = []
        A, B = self._create_individuals()

        self.d.attach_to(A, "2015-10-10T10:10:10+00:00")
        self.d.attach_to(B, "2015-10-10T10:10:10+00:00")

        self.assertEquals(len(self.d.individuals), 1)

        self.assertTrue(self.d.individuals[0]["removed"] == None)

        self._delete_individuals([A, B])

    def test_another_device_can_be_attached_after_removal(self):
        self.d.individuals = []

        A, B = self._create_individuals()
        self.d.attach_to(A, "2015-10-10T10:10:10+00:00")

        self.d.detach_from(A, "2015-10-10T10:10:10+00:00")

        self.assertTrue(self.d.attach_to(B, "2015-10-10T10:10:10+00:00"))

        self._delete_individuals([A,B])


    def test_remove(self):
        self.d.individuals = []
        A, B = self._create_individuals()
        self.d.attach_to(A, "2015-10-10T10:10:10+00:00")
        self.d.detach_from(A, "2015-10-10T10:10:10+00:00")

        self.assertEquals(len(self.d.individuals), 1)
        self.assertTrue(self.d.individuals[0]["removed"] != None)

        self._delete_individuals([A,B])

    def _create_individuals(self):
        return individual.create("LintuA","TaxonA"), individual.create("LintuB","TaxonB")

    def _delete_individuals(self, inds):
        for i in inds:
            i.delete()
