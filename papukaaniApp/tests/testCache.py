from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import PublicPage
from django.conf import settings
from django.core.cache import caches


class TestCache(StaticLiveServerTestCase):

    def setUp(self):
        settings.MOCK_AUTHENTICATION = "Off"
        dev = {
            "deviceManufacturerID": "DeviceId",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "dateCreated": "2015-09-29T14:00:00+03:00",
            "dateEdited": "2015-09-29T14:00:00+03:00"
        }
        self.D = device.create(**dev)

        self.I = individual.create("Birdie", "GAVSTE", description={"fi": "birdiekuvaus"},
                                   descriptionURL={"fi": "http://www.birdie.kek"})

        self.D.attach_to(self.I.id, "1000-01-01T10:00:00+00:00")

        self.page = PublicPage()

        self.lang = settings.LANGUAGE_CODE

        self.page.navigate()

    def tearDown(self):
        self.page.close()
        self.I.delete()
        self.D.delete()

    def test_bird_information_is_cached_in_public(self):

        self.I.nickname = "Burbul"
        self.I.update()

        self.assertTrue("Birdie" in self.page.driver.find_element_by_id("selectIndividual").text)

        self.page.navigate()

        self.assertTrue("Birdie" in self.page.driver.find_element_by_id("selectIndividual").text)

        try:
            caches['public'].clear()
        except:
            pass

        self.page.navigate()

        self.assertTrue("Burbul" in self.page.driver.find_element_by_id("selectIndividual").text)

