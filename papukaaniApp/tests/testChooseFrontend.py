from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from django.test import Client
from papukaaniApp.models import *
from datetime import datetime
from selenium.webdriver.support.expected_conditions import text_to_be_present_in_element
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

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

        self.driver = webdriver.Firefox()
        self.base_url = "http://localhost:8081"
        self.driver.get(self.base_url + '/papukaani/choose')


    def tearDown(self):
        MapPoint.objects.all().delete()

    def test_save_with_button(self):
        button = self.driver.find_element_by_id("save")
        messagebox = self.driver.find_element_by_id("loading")

        button.click()
        self.driver.implicitly_wait(1)

        self.assertTrue(messagebox.text == "Valmis!")

    def test_icon_changes_when_double_clicked(self):
        marker = self.driver.find_elements_by_class_name("leaflet-marker-icon")[0]
        assert "greyMarker.png" in marker.get_attribute("src")

        actionChains = ActionChains(self.driver)
        actionChains.double_click(marker).perform()

        assert "blueMarker.png" in marker.get_attribute("src")


    def test_save_button_is_disabled_while_waiting_for_response(self):
        with open(_filePath + "big.csv") as file:
             Client().post('/papukaani/upload/', {'file': file})

        self.driver.get(self.base_url + '/papukaani/choose')
        button = self.driver.find_element_by_id("save")
        button.click()

        self.assertTrue(not button.is_enabled())




