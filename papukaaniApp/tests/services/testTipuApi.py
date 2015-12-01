from django.test import TestCase
from papukaaniApp.services.lajistore_service import LajiStoreAPI
from papukaani import secret_settings
import sys
from papukaaniApp.services.tipuapi_service import TipuApiAPI


class testTipuApi(TestCase):

    def testGetAll(self):
        response = TipuApiAPI.get_all_species()
        self.assertTrue(str(response).startswith("{'species"))
