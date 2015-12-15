from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from papukaaniApp.tests.test_utils import take_screenshot_of_test_case
from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import ChoosePage
from selenium.webdriver.common.action_chains import ActionChains
import time

_filePath = "papukaaniApp/tests/test_files/"


class TestChooseFrontend(StaticLiveServerTestCase):
    def setUp(self):
        self.A = document.create("TestA", [gathering.Gathering("1234-12-12T12:12:12+00:00", [23.00, 61.00]),
                                           gathering.Gathering("1234-12-12T12:13:14+00:00", [23.01, 61.01])],
                                 "DeviceId")
        dev = {
            "deviceId": "DeviceId",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "createdAt": "2015-09-29T14:00:00+03:00",
            "lastModifiedAt": "2015-09-29T14:00:00+03:00",
            "facts": []
        }
        self.D = device.create(**dev)
        self.page = ChoosePage()

        self.page.navigate()
        self.page.change_device_selection("DeviceId")

    def tearDown(self):
        take_screenshot_of_test_case(self, self.page.driver)
        self.A.delete()
        self.D.delete()
        self.page.close()
        document.delete_all()

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
        self.page.change_device_selection("DeviceId")
        self.assertEquals(0, self.page.number_of_completely_public_clusters_on_map())
        self.assertEquals(0, self.page.number_of_private_clusters_on_map())
        self.assertEquals(1, self.page.number_of_partially_public_clusters_on_map())

    def test_save_button_is_disabled_while_waiting_for_response(self):
        self.page.click_save_button()
        self.assertEquals(not self.page.save_button_is_enabled(), True)

    def test_reset_button_returns_marker_state_to_original(self):
        self.page.double_click_marker()
        self.assertEquals(1, self.page.number_of_completely_public_clusters_on_map())
        self.page.reset()
        self.assertEquals(1, self.page.number_of_private_clusters_on_map())
        self.assertEquals(0, self.page.number_of_completely_public_clusters_on_map())
        self.assertEquals(0, self.page.number_of_partially_public_clusters_on_map())

    def test_reset_button_clears_time_range_fields(self):
        self.page.set_start_time("12-12-1234 00:00")
        self.page.set_end_time("12-12-1234 00:00")
        self.page.reset()
        self.assertEquals(self.page.get_start_time(), '')
        self.assertEquals(self.page.get_end_time(), '')

    def test_device_selector(self):
        self.assertEquals(1, self.page.number_of_private_clusters_on_map())
        self.page.change_device_selection("None")
        self.assertEquals(0, self.page.number_of_private_clusters_on_map())

    def test_filtering_points_with_time_range(self):
        self.page.set_start_time("12-12-1234 12:12")
        self.page.set_end_time("12-12-1234 12:13")
        self.page.show_time_range()
        self.assertEquals(self.page.get_cluster_size(), "0/1")

    def test_filtering_with_end_time_starting_before_start_time_returns_no_points(self):
        self.page.set_start_time("13-12-1234 00:00")
        self.page.set_end_time("12-12-1234 00:00")
        self.page.show_time_range()
        self.assertEquals(self.page.number_of_private_clusters_on_map(), 0)

    def test_popup_is_not_shown_when_no_changes(self):
        self.page.change_device_selection("None")
        self.assertFalse(self.page.popup_displayed())

    def test_popup_is_shown_when_changes(self):
        self.page.double_click_marker()
        self.page.change_device_selection("None")
        self.assertTrue(self.page.popup_displayed())

    def test_changes_are_saved_when_yes_is_pressed(self):
        self.page.double_click_marker()
        self.page.change_device_selection("None")

        self.page.popup_click_yes()
        self.page.change_device_selection("DeviceId")

        self.assertEquals(self.page.number_of_completely_public_clusters_on_map(), 1)

    def test_changes_are_not_saved_when_no_is_pressed(self):
        self.change_publicity_and_selection_without_saving(self)

        self.page.popup_click_no()
        self.page.change_device_selection("DeviceId")

        self.assertEquals(self.page.number_of_completely_public_clusters_on_map(), 0)

    def test_device_selection_does_not_change_when_cancel_is_pressed(self):
        self.change_publicity_and_selection_without_saving(self)

        self.page.popup_click_cancel()
        self.assertEquals(self.page.number_of_completely_public_clusters_on_map(), 1)

        self.assertTrue("DeviceId", self.page.get_device_selection())

    def test_save_button_is_initially_disabled(self):
        self.page.navigate()
        self.assertEquals(self.page.save_button_is_enabled(), False)

    def test_save_button_is_enabled_when_device_with_points_is_selected(self):
        self.assertEquals(self.page.save_button_is_enabled(), True)

    def test_save_button_is_disabled_when_device_with_no_points_is_selected(self):
        self.add_device()
        self.page.navigate()
        self.page.change_device_selection("Empty")
        self.assertEquals(self.page.save_button_is_enabled(), False)
        self.E.delete()

    def test_save_button_is_disabled_after_reset(self):
        self.page.reset()
        self.assertEquals(self.page.save_button_is_enabled(), False)

    def test_disabled_button_cannot_be_clicked(self):
        self.page.driver.execute_script("arguments[0].disabled = 'true';", self.page.RESET_BUTTON)
        self.page.reset()
        self.assertEquals(self.page.number_of_private_clusters_on_map(), 1)

    def add_public_point(self):
        self.A.gatherings.append(gathering.Gathering("1234-12-12T12:12:12+00:00", [23.01, 61.01], publicity="public"))
        self.A.update()

    def add_device(self):
        dev = {
            "deviceId": "Empty",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "createdAt": "2015-09-29T14:00:00+03:00",
            "lastModifiedAt": "2015-09-29T14:00:00+03:00",
            "facts": []
        }
        self.E = device.create(**dev)

    def change_publicity_and_selection_without_saving(self, test):
        test.page.double_click_marker()
        test.page.change_device_selection("None")
