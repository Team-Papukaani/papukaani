from django.test import TestCase
from papukaaniApp.services.lajistore_service import LajiStoreAPI
from papukaaniApp.models_LajiStore import gathering


class testLajiStoreAPI(TestCase):
    def setUp(self):
        self.device = {
            "deviceManufacturerID": "ABCD1234567",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "dateCreated": "2015-09-29T14:00:00+03:00",
            "dateEdited": "2015-09-29T14:00:00+03:00"
        }

        data = [gathering.Gathering("2015-09-15T08:00:00+03:00", [68.93023632, 23.19298104])]
        gatherings = [g.to_lajistore_json() for g in data]
        self.document = {
            "gatherings": gatherings,
            "deviceID": "TestDevice",
            "collectionID": "http://tun.fi/HR.1427",
            "dateCreated": "2015-09-14T15:29:28+03:00",
            "dateEdited": "2015-09-14T15:29:28+03:00",
        }

        self.individual = {
            "nickname": "Lintu1",
            "taxon": "test test"
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

        self.canBeMarkedDeleted()

        response = LajiStoreAPI.delete_individual(response["id"])
        self.assertEquals(204, response.status_code)

    def canBeMarkedDeleted(self):
        self.individual["deleted"] = True
        response = LajiStoreAPI.update_individual(**self.individual)
        self.assertEquals(True, "deleted" in response)

    def testSingleArgumentQueries(self):
        response = LajiStoreAPI.get_all_devices(deviceManufacturerID="ABCD1234567")
        self.assertGreaterEqual(len(response), 0)

        response = LajiStoreAPI.get_all_documents(deviceID="ABCDTESTTEST")
        self.assertGreaterEqual(len(response), 0)

        response = LajiStoreAPI.get_all_individuals(deleted=True)
        self.assertGreaterEqual(len(response), 0)

        response = LajiStoreAPI.get_all_documents(deviceID="NOTFOUND")
        self.assertEqual(len(response), 0)

    def testGetAll(self):
        response = LajiStoreAPI.get_all_documents()
        self.assertGreaterEqual(len(response), 0)

        response = LajiStoreAPI.get_all_devices()
        self.assertGreaterEqual(len(response), 0)

        response = LajiStoreAPI.get_all_individuals()
        self.assertGreaterEqual(len(response), 0)

    def testAddQuery(self):
        q = LajiStoreAPI._add_query(arg1="test")
        self.assertEquals(q, "?q=arg1:test")
        self.assertTrue(" AND " not in q)

        q = LajiStoreAPI._add_query(arg1="test", arg2="value")
        self.assertTrue("arg1:test" in q)
        self.assertTrue("arg2:value" in q)
        self.assertTrue(" AND " in q)

        q = LajiStoreAPI._add_query(arg1="test", arg2="value", arg3=2)
        self.assertTrue("arg1:test" in q)
        self.assertTrue("arg2:value" in q)
        self.assertTrue("arg3:2" in q)
        self.assertTrue(" AND " in q)

    def testAddFilter(self):
        q = LajiStoreAPI._add_query(filter={"arg1": "test"})
        self.assertEquals(q, "?filter=arg1:test")

        q = LajiStoreAPI._add_query(filter={"arg1": "test"}, arg2="test")
        self.assertEquals(q, "?filter=arg1:test&q=arg2:test")
