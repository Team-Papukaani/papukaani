from django.test import TestCase
from papukaaniApp.models_LajiStore import *


class TestDevice(TestCase):
    def setUp(self):
        dev = {
            "deviceId": "ABCD1234567",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "createdAt": "2015-09-29T14:00:00+03:00",
            "lastModifiedAt": "2015-09-29T14:00:00+03:00",
            "facts": []
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

    def test_first_attach(self):
        A, B = self._create_individuals()
        self.d.attach_to(A)
        self.assertEquals(self.d.individuals[0]["individualId"], "A")
        self._delete_individuals([A, B])

    def test_second_attach(self):
        self.d.individuals = []
        A, B = self._create_individuals()

        self.d.attach_to(A)
        self.d.attach_to(B)

        self.assertEquals(len(self.d.individuals), 2)

        self.assertTrue(self.d.individuals[0]["removed"] != None)

        self._delete_individuals([A, B])

    def test_remove(self):
        self.d.individuals = []
        A, B = self._create_individuals()
        self.d.attach_to(A)
        self.d.remove_from(A)

        self.assertEquals(len(self.d.individuals), 1)
        self.assertTrue(self.d.individuals[0]["removed"] != None)

    def _create_individuals(self):
        return individual.create("A", "Taxon"), individual.create("B", "Taxon")

    def _delete_individuals(self, inds):
        for i in inds:
            i.delete()
