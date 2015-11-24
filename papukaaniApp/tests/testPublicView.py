import time

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.wait import WebDriverWait

from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import PublicPage
from papukaaniApp.tests.test_utils import take_screenshot_of_test_case


class PublicView(StaticLiveServerTestCase):
    def setUp(self):
        self.A = document.create("TestA",
                                 [gathering.Gathering("1234-12-12T12:12:12+00:00", [64.0, 26.0].reverse(), publicity="public"),
                                  gathering.Gathering("1235-12-12T12:13:12+00:00", [40.01, 13.01].reverse(), publicity="public"),
                                  gathering.Gathering("1235-12-12T12:13:12+00:00", [61.01, 43.01].reverse(), publicity="public")], "DeviceId")
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

    def test_marker_moves_when_play_is_pressed(self):
        self.page.play_animation_for_device('DeviceId')
        start_location = self.page.SINGLE_MARKER.location

        def marker_moving():
            print(self.page.SINGLE_MARKER.location)
            return start_location != self.page.SINGLE_MARKER.location

        WebDriverWait(self.page.driver, 15).until(marker_moving)

    def test_no_points_are_shown_on_map(self):
        self.assertEquals(self.page.get_number_of_points(), 0)

    def test_can_choose_points_by_device(self):
        self.page.change_device_selection("DeviceId")
        self.page.PLAY.click()
        self.page.play()
        self.assertNotEquals(self.page.POLYLINE, None)

    def test_polylines_are_cleared_on_selection_change(self):
        self.test_can_choose_points_by_device()
        self.page.PAUSE.click()
        self.page.change_device_selection("None")

    def test_pause_stops_polyline_drawing(self):
        self.test_can_choose_points_by_device()
        self.page.PAUSE.click()
        start = self.page.get_map_polyline_elements()
        time.sleep(1)
        self.assertEquals(start, self.page.get_map_polyline_elements())
