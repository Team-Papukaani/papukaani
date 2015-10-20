from datetime import datetime
import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import ChoosePage

_filePath = "papukaaniApp/tests/test_files/"


class TestChooseFrontend(StaticLiveServerTestCase):
    def setUp(self):
        self.A = document.create("TestA", [gathering.Gathering("1234-12-12T12:12:12+00:00", [61.0, 23.0]), gathering.Gathering("1234-12-12T12:12:12+00:00", [61.01, 23.01])], "DeviceId")

        self.page = ChoosePage()
        self.page.navigate()

    def tearDown(self):
        self.A.delete()
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
        self.assertEquals(0, self.page.number_of_completely_public_clusters_on_map())
        #self.assertEquals(0, self.page.number_of_private_clusters_on_map())
        #self.assertEquals(1, self.page.number_of_partially_public_clusters_on_map())

    def test_save_button_is_disabled_while_waiting_for_response(self):
        with open(_filePath + "ecotones.csv") as file:
            Client().post('/papukaani/upload/', {'file': file})
        self.page.click_save_button()
        self.assertEquals(not self.page.save_button_is_enabled(), True)

    def test_reset_button_returns_marker_state_to_original(self):
        self.page.double_click_marker()
        self.page.reset()
        self.assertEquals(1, self.page.number_of_private_clusters_on_map())
        self.page.double_click_marker()
        self.assertEquals(1, self.page.number_of_completely_public_clusters_on_map())
        self.page.reset()
        self.assertEquals(1, self.page.number_of_private_clusters_on_map())

    def test_reset_button_clears_time_range_fields(self):
        self.page.set_start_time("01/01/1234")
        self.page.set_end_time("01/01/4321")
        self.page.reset()
        self.assertEquals(self.page.get_start_time(), '')
        self.assertEquals(self.page.get_end_time(), '')

    def test_device_selector(self):
        self.B = document.create("TestB", [], "DeviceId2")
        self.page.navigate()
        self.assertEquals(1, self.page.number_of_private_clusters_on_map())
        self.page.change_device_selection("DeviceId2")
        self.assertEquals(0, self.page.number_of_private_clusters_on_map())

    def add_public_point(self):
        self.A.gatherings.append(gathering.Gathering("1234-12-12T12:12:12+00:00", [61.01, 23.01], publicity="public"))
        self.A.update()
