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

    def test_create(self):
        self.assertEquals("ABCD1234567", self.d.deviceManufacturerID)
        self.assertEquals("Type", self.d.deviceType)
        self.assertEquals("Manufacturer", self.d.deviceManufacturer)

    def test_update_and_get(self):
        self.d.deviceType = "NewType"
        self.d.update()
        gotten = device.get(self.d.id)
        self.assertEquals("NewType", gotten.deviceType)

    def test_get_all(self):
        self.assertGreater(len(device.find()), 0)

    def test_create_does_not_make_duplicates(self):
        before = len(device.find())
        dev = {
            "deviceManufacturerID": "ABCD1234567",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "dateCreated": "2015-09-29T14:00:00+03:00",
            "dateEdited": "2015-09-29T14:00:00+03:00"
        }
        device.create(**dev)
        self.assertEquals(before, len(device.find()))

        dev2 = {
            "deviceManufacturerID": "TESTTEST",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "dateCreated": "2015-09-29T14:00:00+03:00",
            "dateEdited": "2015-09-29T14:00:00+03:00"
        }
        d = device.create(**dev2)
        self.assertLess(before, len(device.find()))

        d.delete()

    def test_attach(self):
        A, B = self._create_individuals()
        self.d.attach_to(A.id, "2015-10-10T10:10:10+00:00")
        self.assertEquals(A.id, self.d.get_attached_individualid())
        self._delete_individuals([A, B])

    def test_device_not_attach_if_unremoved_devices_in_individuals(self):
        self.d.individuals = []

        A, B = self._create_individuals()
        self.d.attach_to(A.id, "2015-10-10T10:10:10+00:00")
        self.d.attach_to(B.id, "2015-10-10T10:10:10+00:00")
        individuals = self.d.get_individuals_for_device()

        self.assertEquals(len(individuals), 1)
        self.assertTrue(individuals[0]["removed"] is None)

        self._delete_individuals([A, B])

    def test_another_device_can_be_attached_after_removal(self):
        self.d.individuals = []

        A, B = self._create_individuals()
        self.d.attach_to(A.id, "2015-10-10T10:10:10+00:00")
        self.d.detach_from(A.id, "2015-10-10T10:10:10+00:00")
        self.assertTrue(self.d.attach_to(B.id, "2015-10-10T10:10:10+00:00") is None)

        self._delete_individuals([A, B])

    def test_remove(self):
        A, B = self._create_individuals()
        self.d.attach_to(A.id, "2015-10-10T10:10:10+00:00")
        self.d.detach_from(A.id, "2015-10-10T10:10:10+00:00")
        individuals = self.d.get_individuals_for_device()
        self.assertEquals(len(individuals), 1)
        self.assertTrue(individuals[0]["removed"] is not None)

        self._delete_individuals([A, B])

    def test_getting_attached_individualid(self):
        A, B = self._create_individuals()
        self.d.attach_to(A.id, "2015-10-10T10:10:10+00:00")
        id = self.d.get_attached_individualid()
        self.assertEqual(id, A.id)

        self._delete_individuals([A, B])

    def test_getting_individuals(self):
        A, B = self._create_individuals()
        self.d.attach_to(A.id, "2015-10-10T10:10:10+00:00")
        self.d.detach_from(A.id, "2015-10-10T10:10:10+00:01")
        self.d.attach_to(B.id, "2015-10-10T10:10:10+00:02")
        individuals = self.d.get_individuals_for_device()
        self.assertEquals(len(individuals), 2)

        self._delete_individuals([A, B])

    def test_checking_if_an_individual_is_attached(self):
        self.assertFalse(self.d.get_attached_individualid())

        A, B = self._create_individuals()
        self.d.attach_to(A.id, "2015-10-10T10:10:10+00:00")
        self.assertTrue(self.d.get_attached_individualid())

        self._delete_individuals([A, B])

    def _create_individuals(self):
        return individual.create("LintuA", "TaxonA"), individual.create("LintuB", "TaxonB")

    def _delete_individuals(self, inds):
        for i in inds:
            i.delete()