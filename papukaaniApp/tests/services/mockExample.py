from django.test import TestCase
from papukaaniApp.services.lajistore_service import LajiStoreAPI
from . import LajiStoreMock


class mockExample(TestCase):
    LajiStoreAPI = LajiStoreMock

    def exampleTest(self):
        self.assertEquals({
            "id": 1,
            "individualId": "INDIVIDUALABCD",
            "taxon": "test test"
        }, LajiStoreAPI.get_individual(1))
