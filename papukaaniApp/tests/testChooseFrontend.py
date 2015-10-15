from datetime import datetime
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
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
        MapPoint.objects.create(
            creature=self.creature,
            gpsNumber=1,
            latitude=61.01,
            longitude=23.01,
            altitude=222.22,
            temperature=22.2,
            timestamp=datetime.now()
        )

        self.page = ChoosePage()
        self.page.navigate()

    def tearDown(self):
        MapPoint.objects.all().delete()
        self.page.close()

    def test_save_with_button(self):
        self.page.click_save_button()
        WebDriverWait(self.page.driver, 60).until(
            EC.text_to_be_present_in_element((By.ID, "loading"), "Valmis!")
        )

    def test_icon_changes_when_double_clicked(self):
        markers = self.page.number_of_completely_public_clusters_on_map()
        self.page.double_click_marker()
        self.assertEquals(markers + 1, self.page.number_of_completely_public_clusters_on_map())

    def test_cluster_with_only_public_points_is_green(self):
        time.sleep(10)
        self.page.double_click_marker()
        self.assertEquals(1, self.page.number_of_completely_public_clusters_on_map())
        self.assertEquals(0, self.page.number_of_private_clusters_on_map())
        self.assertEquals(0, self.page.number_of_partially_public_clusters_on_map())

    def test_cluster_initially_contains_only_private_points_and_is_grey(self):
        self.assertEquals(0, self.page.number_of_completely_public_clusters_on_map())
        self.assertEquals(1, self.page.number_of_private_clusters_on_map())
        self.assertEquals(0, self.page.number_of_partially_public_clusters_on_map())

    def test_cluster_with_mixed_public_and_private_points_is_yellow(self):
        self.add_public_point()
        self.page.navigate()
        time.sleep(10)
        self.assertEquals(0, self.page.number_of_completely_public_clusters_on_map())
        self.assertEquals(0, self.page.number_of_private_clusters_on_map())
        self.assertEquals(1, self.page.number_of_partially_public_clusters_on_map())

    def test_save_button_is_disabled_while_waiting_for_response(self):
        with open(_filePath + "big.csv") as file:
            Client().post('/papukaani/upload/', {'file': file})
        self.page.click_save_button()
        self.assertEquals(not self.page.save_button_is_enabled(), True)

    def add_public_point(self):
        MapPoint.objects.create(
            creature=self.creature,
            gpsNumber=1,
            latitude=61.01,
            longitude=23.02,
            altitude=222.22,
            temperature=22.2,
            timestamp=datetime.now(),
            public=True
        )
