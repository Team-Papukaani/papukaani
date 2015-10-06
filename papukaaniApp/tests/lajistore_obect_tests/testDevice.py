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




