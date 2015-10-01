from datetime import datetime

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.test import Client
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.support import expected_conditions as EC

from papukaaniApp.models import *
from papukaaniApp.tests.page_models.page_models import ChoosePage

_filePath = "papukaaniApp/tests/test_files/"


class TestChooseFrontend(StaticLiveServerTestCase):
    def setUp(self):
        self.creature = Creature.objects.create(name="Creature")
        self.A = MapPoint.objects.create(
            creature=self.creature,
            gpsNumber=1,
            latitude=61.00,
            longitude=23.00,
            altitude=222.22,
            temperature=22.2,
            timestamp=datetime.now(),
        )

        self.driver = webdriver.PhantomJS()
        self.page = ChoosePage(self.driver)
        self.page.navigate()

    def tearDown(self):
        MapPoint.objects.all().delete()
        self.driver.close()

    def test_save_with_button(self):
        self.page.click_save_button()
        WebDriverWait(self.driver, 60).until(
            EC.text_to_be_present_in_element((By.ID, "loading"), "Valmis!")
        )

    def test_icon_changes_when_double_clicked(self):
        self.assertEquals("greyMarker.png" in self.page.get_marker_src(), 1)
        self.page.double_click_marker()
        self.assertEquals("blueMarker.png" in self.page.get_marker_src(), 1)

    def test_save_button_is_disabled_while_waiting_for_response(self):
        with open(_filePath + "big.csv") as file:
            Client().post('/papukaani/upload/', {'file': file})
        self.page.click_save_button()
        self.assertTrue(not self.page.save_button_is_enabled())
