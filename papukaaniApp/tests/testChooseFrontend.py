from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import ChoosePage
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

    """
    def test_reset_button_returns_marker_state_to_original(self):
        self.page.double_click_marker()
        self.page.reset()
        self.assertEquals(1, self.page.number_of_private_clusters_on_map())
        self.page.double_click_marker()
        self.assertEquals(1, self.page.number_of_completely_public_clusters_on_map())
        self.page.reset()
        self.assertEquals(1, self.page.number_of_private_clusters_on_map())
    """

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

    def add_public_point(self):
        self.A.gatherings.append(gathering.Gathering("1234-12-12T12:12:12+00:00", [23.01, 61.01], publicity="public"))
        self.A.update()
