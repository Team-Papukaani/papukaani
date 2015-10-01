from django.test import TestCase
from papukaaniApp.services.lajistore_service import LajiStoreAPI

class testLajiStoreAPI(TestCase):


    def setUp(self):
        self.device = {
                           "deviceId": "ABCD1234567",
                           "deviceType": "Type",
                           "deviceManufacturer": "Manufacturer",
                           "createdAt": "2015-09-29T14:00:00+03:00",
                           "createdBy": "SomeUser",
                           "lastModifiedAt": "2015-09-29T14:00:00+03:00",
                           "lastModifiedBy": "SomeUser",
                           "facts": []
                        }

        self.document = {
                            "lastModifiedAt": "2015-09-15T11:25:58+03:00",
                            "lastModifiedBy": "SomeUser",
                            "documentId": "ABCDTESTTEST",

                            "createdAt": "2015-09-15T11:25:58+03:00",
                            "createdBy": "SomeUser",
                            "facts": [],
                            "gatherings": [],
                        }

    def testLajiStoreDevice(self):

        response = LajiStoreAPI.post_device(**self.device)
        self.assertEquals(True, "id" in response)

        response = LajiStoreAPI.get_device(response["id"])
        self.assertEquals(True, "id" in response)

        self.device["id"] = response["id"]
        response = LajiStoreAPI.update_device(**self.device)
        self.assertEquals(True, "id" in response)

        response = LajiStoreAPI.delete_device(response["id"])
        self.assertEquals(204, response.status_code)

    def testLajiStoreDocument(self):

        response = LajiStoreAPI.post_document(**self.document)
        self.assertEquals(True, "id" in response)

        response = LajiStoreAPI.get_document(response["id"])
        self.assertEquals(True, "id" in response)

        self.document["id"] = response["id"]
        response = LajiStoreAPI.update_document(**self.document)

        self.assertEquals(True, "id" in response)

        response = LajiStoreAPI.delete_document(response["id"])
        self.assertEquals(204, response.status_code)

