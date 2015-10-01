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

        self.individual = {
                            "individualId" : "INDIVIDUALABCD",
                            "taxon" : "test test"
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

    def testLajiStoreIndividual(self):

        response = LajiStoreAPI.post_individual(**self.individual)
        self.assertEquals(True, "id" in response)

        response = LajiStoreAPI.get_individual(response["id"])
        self.assertEquals(True, "id" in response)

        self.individual["id"] = response["id"]
        response = LajiStoreAPI.update_individual(**self.individual)
        self.assertEquals(True, "id" in response)

        response = LajiStoreAPI.delete_individual(response["id"])
        self.assertEquals(204, response.status_code)

    def testSingleArgumentQueries(self):

        response = LajiStoreAPI.get_all_devices(deviceType="Type")
        self.assertGreaterEqual(len(response), 0)

        response = LajiStoreAPI.get_all_documents(arg="TEST1234")
        self.assertGreaterEqual(len(response), 0)

        response = LajiStoreAPI.get_all_individuals(arg="TEST123")
        self.assertGreaterEqual(len(response), 0)

    def testMultipleArgumentQueries(self):

        response = LajiStoreAPI.get_all_documents(something="TEST1234", testtest=[])
        self.assertGreaterEqual(len(response), 0)

        response = LajiStoreAPI.get_all_devices(param="Type", param2="A123TEsT", deviceManufacturer="Manu")
        self.assertGreaterEqual(len(response), 0)


        response = LajiStoreAPI.get_all_individuals(param="IDIDIDI", taxon="test test" )
        self.assertGreaterEqual(len(response), 0)

    def testGetAll(self):
        response = LajiStoreAPI.get_all_documents()
        self.assertGreaterEqual(len(response), 0)

        response = LajiStoreAPI.get_all_devices()
        self.assertGreaterEqual(len(response), 0)

        response = LajiStoreAPI.get_all_individuals()
        self.assertGreaterEqual(len(response), 0)

    def testAddQuery(self):
        q = LajiStoreAPI._add_query(arg1 = "test")
        self.assertEquals(q, "?query=arg1:test")
        self.assertTrue(" AND " not in q)

        q = LajiStoreAPI._add_query(arg1 = "test", arg2="value")
        self.assertTrue("arg1:test" in q)
        self.assertTrue("arg2:value" in q)
        self.assertTrue(" AND " in q)

        q = LajiStoreAPI._add_query(arg1 = "test", arg2="value", arg3=2)
        self.assertTrue("arg1:test" in q)
        self.assertTrue("arg2:value" in q)
        self.assertTrue("arg3:2" in q)
        self.assertTrue(" AND " in q)

