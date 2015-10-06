from django.test import TestCase
from papukaaniApp.models_LajiStore import device


class TestDevice(TestCase):

    def setUp(self):

        dev = {
        "deviceId": "ABCD1234567",
        "deviceType": "Type",
        "deviceManufacturer": "Manufacturer",
        "createdAt": "2015-09-29T14:00:00+03:00",
        "createdBy": "SomeUser",
        "lastModifiedAt": "2015-09-29T14:00:00+03:00",
        "lastModifiedBy": "SomeUser",
        "facts": []

        }
        self.d = device.create(**dev)

    def tearDown(self):
        self.d.delete()

    def testCreateAndDelete(self):
        self.assertEquals("ABCD1234567", self.d.deviceId)
        self.assertEquals("Type", self.d.deviceType)
        self.assertEquals("Manufacturer", self.d.deviceManufacturer)

    def testUpdateAndGet(self):
        self.d.deviceType = "NewType"
        self.d.update()
        gotten = device.get(self.d.id)
        self.assertEquals("NewType", gotten.deviceType)





