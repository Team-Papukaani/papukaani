import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import PublicPage
from papukaaniApp.tests.test_utils import take_screenshot_of_test_case
from datetime import datetime


class PublicView(StaticLiveServerTestCase):
    def setUp(self):
        self.A = document.create("TestA",
                                 [gathering.Gathering("1234-12-12T12:12:12+00:00", [23.00, 61.00], publicity="public"),
                                  gathering.Gathering("1234-12-12T12:13:12+00:00", [23.01, 61.01],
                                                      publicity="private")], "DeviceId")
        dev = {
            "deviceId": "DeviceId",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "createdAt": "2015-09-29T14:00:00+03:00",
            "lastModifiedAt": "2015-09-29T14:00:00+03:00",
            "facts": []
        }
        self.D = device.create(**dev)
        self.page = PublicPage()
        self.page.navigate()

    def tearDown(self):
        take_screenshot_of_test_case(self, self.page.driver)
        self.page.close()
        self.A.delete()
        self.D.delete()

    def test_no_points_are_shown_on_map(self):
        self.assertEquals(self.page.get_number_of_points(), 0)

    def test_can_choose_points_by_device(self):
        self.select_device_and_play()
        self.assertNotEquals(self.page.POLYLINE, None)

    def test_polylines_are_cleared_on_selection_change(self):
        self.select_device_and_play()
        self.page.PAUSE.click()
        self.page.change_device_selection("None")

    def test_pause_stops_polyline_drawing(self):
        self.select_device_and_play()
        self.page.PAUSE.click()
        start = self.page.get_map_polyline_elements()
        time.sleep(1)
        self.assertEquals(start, self.page.get_map_polyline_elements())

    def test_marker_has_popup(self):
        self.page.change_device_selection("DeviceId")
        self.page.get_marker().click()
        self.assertNotEquals(self.page.get_popup(), None)

    def select_device_and_play(self):
        self.page.change_device_selection("DeviceId")
        self.page.play()

    def test_slider_is_created_when_device_is_selected(self):
        self.page.change_device_selection("DeviceId")
        self.assertEquals(len(self.page.driver.find_elements_by_class_name("ui-slider")), 2)
        self.assertEquals(self.page.driver.find_element_by_id("playLabel").get_attribute("innerHTML"),
                          "1234/12/12 12:12:12")

    def test_slider_label_value_changes_when_playing(self):
        self.select_device_and_play()
        time.sleep(1)
        label = self.page.driver.find_element_by_id("playLabel")
        self.assertEquals(label.get_attribute("innerHTML"), "1234/12/12 12:13:12")
