import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.wait import WebDriverWait

from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import PublicPage
from papukaaniApp.tests.test_utils import take_screenshot_of_test_case
from django.conf import settings

class PublicView(StaticLiveServerTestCase):
    def setUp(self):
        self.A = document.create("TestA",
                                 [gathering.Gathering("1234-12-12T12:12:12+00:00", [23.00, 61.00], publicity="public"),
                                  gathering.Gathering("1234-12-12T12:13:12+00:00", [63.01, 61.01],
                                                      publicity="public")], "DeviceId")
        self.B = document.create("TestB",
                                 [gathering.Gathering("1235-12-12T12:12:12+00:00", [23.00, 61.00], publicity="public")], "DeviceId2")
        dev = {
            "deviceId": "DeviceId",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "createdAt": "2015-09-29T14:00:00+03:00",
            "lastModifiedAt": "2015-09-29T14:00:00+03:00",
            "facts": []
        }
        dev2 = {
            "deviceId": "DeviceId2",
            "deviceType": "Type",
            "deviceManufacturer": "Google",
            "createdAt": "2014-09-29T14:00:00+03:00",
            "lastModifiedAt": "2014-09-29T14:00:00+03:00",
            "facts": []
        }
        self.D = device.create(**dev)
        self.D2 = device.create(**dev2)
        self.page = PublicPage()
        self.page.navigate()

    def tearDown(self):
        take_screenshot_of_test_case(self, self.page.driver)
        self.page.close()
        self.A.delete()
        self.D.delete()

    def test_marker_moves_when_play_is_pressed(self):
        self.page.play_animation_for_device('DeviceId')
        start_location = self.page.SINGLE_MARKER.location

        def marker_is_moving(driver):
            current_location = self.page.SINGLE_MARKER.location
            return abs(start_location['x'] - current_location['x']) > 40

        WebDriverWait(self.page.driver, 15).until(marker_is_moving)

    def test_no_points_are_shown_on_map_initially(self):
        self.assertEquals(self.page.get_number_of_points(), 0)

    def test_can_choose_points_by_device(self):
        self.select_device_and_play()
        self.assertNotEquals(self.page.POLYLINE, None)

    def test_polylines_are_cleared_on_selection_change(self):
        self.select_device_and_play()
        self.page.play()
        self.page.change_device_selection("None")

    def test_pause_stops_polyline_drawing(self):
        self.select_device_and_play()
        self.page.play()
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

    def test_slider_label_value_changes_when_playing(self):
        self.select_device_and_play()
        time.sleep(1)
        label = self.page.driver.find_element_by_id("playLabel")
        self.assertNotEquals(label.get_attribute("innerHTML"), "1234/12/12 12:12:12")

    def test_polyline_is_drawn_when_playing(self):
        self.select_device_and_play()
        startcount = len(self.page.driver.find_elements_by_tag_name("g"))
        time.sleep(1)
        self.assertGreater(startcount, len(self.page.driver.find_elements_by_class_name("g")))

    def test_navigation_is_shown_if_logged_in(self):
        settings.MOCK_AUTHENTICATION = "On"
        try:
            self.page.get_navigation()
        except:
            self.fail()

    def test_navigation_is_not_shown_if_logged_in(self):
        settings.MOCK_AUTHENTICATION = "Skip"
        try:
            self.page.get_navigation()
            self.fail()
        except:
            pass

    def test_speed_sets_with_param(self):
        self.assertEquals('75', self.page.get_speed_set_as_param(75))