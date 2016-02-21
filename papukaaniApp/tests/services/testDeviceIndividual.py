from django.test import TestCase
from papukaaniApp.services.deviceindividual_service import DeviceIndividual
from papukaaniApp.models_LajiStore import individual, device


class testDeviceIndividual(TestCase):
    def setUp(self):
        DeviceIndividual.delete_all()
        self.D = device.create(**{
            "deviceManufacturerID": "ABCD1234567",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "dateCreated": "2015-09-29T14:00:00+03:00",
            "dateEdited": "2015-09-29T14:00:00+03:00"
        })
        self.D2 = device.create(**{
            "deviceManufacturerID": "ABCD1234568",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "dateCreated": "2015-09-29T14:00:00+03:00",
            "dateEdited": "2015-09-29T14:00:00+03:00"
        })

        self.I = individual.create("Lintu1", "test")
        self.I2 = individual.create("Lintu2", "test")

    def tearDown(self):
        self.D.delete()
        self.D2.delete()
        self.I.delete()
        self.I2.delete()
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
        self.assertEquals(self.I.id, DeviceIndividual.get_attached_individual(self.D.id)["individualID"])
        self.assertEquals(self.I.id, DeviceIndividual.get_attached_individual(self.D.id)["individualID"])
        self.assertEquals("2015-09-29T14:00:00+03:00", DeviceIndividual.get_attached_device(self.I.id)["attached"])
        self.assertEquals("2015-09-29T14:00:00+03:00", DeviceIndividual.get_attached_device(self.I.id)["attached"])

    def testAttachTwo(self):
        self.assertEquals(0, len(DeviceIndividual.find()))
        DeviceIndividual.attach(self.D.id, self.I.id, "2015-09-29T14:00:00+03:00")
        self.assertEquals(1, len(DeviceIndividual.find()))
        DeviceIndividual.attach(self.D2.id, self.I2.id, "2015-09-29T14:00:00+03:00")
        self.assertEquals(2, len(DeviceIndividual.find()))
        self.assertEquals(self.I.id, DeviceIndividual.get_attached_individual(self.D.id)["individualID"])
        self.assertEquals(self.D.id, DeviceIndividual.get_attached_device(self.I.id)["deviceID"])
        self.assertEquals(self.I2.id, DeviceIndividual.get_attached_individual(self.D2.id)["individualID"])
        self.assertEquals(self.D2.id, DeviceIndividual.get_attached_device(self.I2.id)["deviceID"])

    def testAttachTwiceDoesNotAttachAgain(self):
        self.assertEquals(0, len(DeviceIndividual.find()))
        DeviceIndividual.attach(self.D.id, self.I.id, "2015-09-29T14:00:00+03:00")
        self.assertEquals(1, len(DeviceIndividual.find()))
        DeviceIndividual.attach(self.D.id, self.I.id, "2015-09-29T14:00:00+03:00")
        self.assertEquals(1, len(DeviceIndividual.find()))

    def testAttachToAnotherDeviceDoesNotAttach(self):
        DeviceIndividual.attach(self.D.id, self.I.id, "2015-09-29T14:00:00+03:00")
        self.assertEquals(1, len(DeviceIndividual.find()))
        DeviceIndividual.attach(self.D2.id, self.I.id, "2015-09-29T14:00:00+03:00")
        self.assertEquals(1, len(DeviceIndividual.find()))

    def testAttachToAnotherIndividualDoesNotAttach(self):
        DeviceIndividual.attach(self.D.id, self.I.id, "2015-09-29T14:00:00+03:00")
        self.assertEquals(1, len(DeviceIndividual.find()))
        DeviceIndividual.attach(self.D.id, self.I2.id, "2015-09-29T14:00:00+03:00")
        self.assertEquals(1, len(DeviceIndividual.find()))

    def testAttachDetachOne(self):
        self.assertEquals(0, len(DeviceIndividual.find()))

        DeviceIndividual.attach(self.D.id, self.I.id, "2015-09-29T14:00:00+03:00")

        self.assertEquals(1, len(DeviceIndividual.find()))
        self.assertEquals(self.I.id, DeviceIndividual.get_attached_individual(self.D.id)["individualID"])
        self.assertEquals(self.D.id, DeviceIndividual.get_attached_device(self.I.id)["deviceID"])
        self.assertEquals(None, DeviceIndividual.get_attached_individual(self.D.id)["removed"])
        self.assertEquals(None, DeviceIndividual.get_attached_device(self.I.id)["removed"])

        DeviceIndividual.detach(self.D.id, self.I.id, "2015-09-29T14:00:00+03:00")

        self.assertEquals("2015-09-29T14:00:00+03:00", DeviceIndividual.get_individuals_for_device(self.D.id)[0]["removed"])
        self.assertEquals("2015-09-29T14:00:00+03:00", DeviceIndividual.get_devices_for_individual(self.I.id)[0]["removed"])
        self.assertEquals(1, len(DeviceIndividual.find()))
        self.assertEquals(None, DeviceIndividual.get_attached_individual(self.D.id))
        self.assertEquals(None, DeviceIndividual.get_attached_device(self.I.id))

    def testAttachDetachTwo(self):
        self.assertEquals(0, len(DeviceIndividual.find()))

        DeviceIndividual.attach(self.D.id, self.I.id, "2015-09-29T14:00:00+03:00")
        DeviceIndividual.attach(self.D2.id, self.I2.id, "2015-09-29T14:00:00+03:00")

        self.assertEquals(2, len(DeviceIndividual.find()))
        self.assertEquals(self.I.id, DeviceIndividual.get_attached_individual(self.D.id)["individualID"])
        self.assertEquals(self.D.id, DeviceIndividual.get_attached_device(self.I.id)["deviceID"])
        self.assertEquals(self.I2.id, DeviceIndividual.get_attached_individual(self.D2.id)["individualID"])
        self.assertEquals(self.D2.id, DeviceIndividual.get_attached_device(self.I2.id)["deviceID"])

        DeviceIndividual.detach(self.D.id, self.I.id, "2015-09-29T14:00:00+03:00")

        self.assertEquals(None, DeviceIndividual.get_attached_individual(self.D.id))
        self.assertEquals(None, DeviceIndividual.get_attached_device(self.I.id))
        self.assertEquals(self.I2.id, DeviceIndividual.get_attached_individual(self.D2.id)["individualID"])
        self.assertEquals(self.D2.id, DeviceIndividual.get_attached_device(self.I2.id)["deviceID"])

        DeviceIndividual.detach(self.D2.id, self.I2.id, "2015-09-29T14:00:00+03:00")

        self.assertEquals(None, DeviceIndividual.get_attached_individual(self.D2.id))
        self.assertEquals(None, DeviceIndividual.get_attached_device(self.I2.id))
        self.assertEquals(2, len(DeviceIndividual.find()))

    def testGetAllAttachedIndividuals(self):
        self.assertEquals(0, len(DeviceIndividual.find()))

        DeviceIndividual.attach(self.D.id, self.I.id, "2015-09-29T14:00:00+03:00")
        DeviceIndividual.detach(self.D.id, self.I.id, "2015-09-29T14:00:00+03:00")
        DeviceIndividual.attach(self.D.id, self.I2.id, "2015-09-29T14:00:00+03:00")

        self.assertEquals(2, len(DeviceIndividual.get_individuals_for_device(self.D.id)))
        self.assertEquals(self.I2.id, DeviceIndividual.get_attached_individual(self.D.id)["individualID"])

    def testDeletedDevicesDontStopNewAttachments(self):
        DeviceIndividual.attach(self.D.id, self.I.id, "2015-09-29T14:00:00+03:00")
        self.D.delete();
        DeviceIndividual.attach(self.D2.id, self.I.id, "2015-09-29T14:00:00+03:00")
        self.assertEquals(self.D2.id, DeviceIndividual.get_attached_device(self.I.id)['deviceID'])

    def testDeletedIndividualsDontStopNewAttachments(self):
        DeviceIndividual.attach(self.D.id, self.I.id, "2015-09-29T14:00:00+03:00")
        self.I.delete();
        DeviceIndividual.attach(self.D.id, self.I2.id, "2015-09-29T14:00:00+03:00")
        self.assertEquals(self.I2.id, DeviceIndividual.get_attached_individual(self.D.id)['individualID'])

