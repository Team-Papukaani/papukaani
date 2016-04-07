import time
import json
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import PublicPage
from papukaaniApp.tests.test_utils import take_screenshot_of_test_case
from django.conf import settings
import dateutil.parser


class PublicView(StaticLiveServerTestCase):
    def setUp(self):
        dev = {
            "deviceManufacturerID": "DeviceId",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "dateCreated": "2015-09-29T14:00:00+03:00",
            "dateEdited": "2015-09-29T14:00:00+03:00"
        }
        dev2 = {
            "deviceManufacturerID": "DeviceId2",
            "deviceType": "Type",
            "deviceManufacturer": "Google",
            "dateCreated": "2014-09-29T14:00:00+03:00",
            "dateEdited": "2014-09-29T14:00:00+03:00"
        }

        self.I = individual.create("Birdie", "GAVSTE", description={"fi": "birdiekuvaus"},
                                   descriptionURL={"fi": "http://www.birdie.kek"})
        self.I2 = individual.create("Birdie2", "GAVSTE")

        self.D = device.create(**dev)
        self.D2 = device.create(**dev2)

        self.D.attach_to(self.I.id, "1000-01-01T10:00:00+00:00")
        self.D2.attach_to(self.I2.id, "1000-01-01T10:00:00+00:00")

        self.A = document.create(
            [gathering.Gathering("2010-11-16T00:00:00+00:00", [23.00, 61.00],
                                 publicityRestrictions="MZ.publicityRestrictionsPublic"),
             gathering.Gathering("2010-12-11T00:00:00+00:00", [63.01, 61.01],
                                 publicityRestrictions="MZ.publicityRestrictionsPublic"),
             gathering.Gathering("2010-12-13T00:00:00+00:00", [65.01, 61.01],
                                 publicityRestrictions="MZ.publicityRestrictionsPublic"),
             gathering.Gathering("2010-12-15T00:00:00+00:00", [68.01, 61.01],
                                 publicityRestrictions="MZ.publicityRestrictionsPublic")
             ], self.D.id)
        self.B = document.create(
            [gathering.Gathering("2010-12-12T12:12:12+00:00", [23.00, 61.00],
                                 publicityRestrictions="MZ.publicityRestrictionsPublic")],
            self.D2.id)

        self.page = PublicPage()
        self.page.navigate()

        self.lang = settings.LANGUAGE_CODE

        with open('papukaaniApp/tests/test_files/canvas.json', encoding='utf-8') as data:
            self.canvas = json.loads(data.read())

    def tearDown(self):
        take_screenshot_of_test_case(self, self.page.driver)
        self.page.close()
        self.I.delete()
        self.I2.delete()
        self.A.delete()
        self.D.delete()
        self.B.delete()
        self.D2.delete()

    def test_marker_moves_when_play_is_pressed(self):
        self.page.play_animation_for_individual(str(self.I.id))
        start_location = self.page.SINGLE_MARKER.location

        def marker_is_moving(driver):
            current_location = self.page.SINGLE_MARKER.location
            return abs(start_location['x'] - current_location['x']) > 40

        WebDriverWait(self.page.driver, 15).until(marker_is_moving)

    def test_no_points_are_shown_on_map_initially(self):
        self.assertEquals(self.page.get_number_of_points(), 0)

    def test_can_choose_points_by_individual(self):
        self.select_individual_and_play()
        self.assertNotEquals(self.page.POLYLINE, None)

    def test_polylines_are_cleared_on_select_and_delete(self):
        self.page.change_individual_selection(str(self.I.id))
        self.page.change_individual_selection(str(self.I2.id))
        self.page.remove_selected_individual(str(self.I.id))
        time.sleep(1)
        self.page.remove_selected_individual(str(self.I2.id))
        time.sleep(1)
        self.assertEquals(len(self.page.driver.find_elements_by_tag_name("g")), 0)

    def test_pause_stops_polyline_drawing(self):
        self.select_individual_and_play()
        time.sleep(1)
        self.page.play()
        start = self.page.get_map_polyline_elements()
        time.sleep(1)
        self.assertEquals(start, self.page.get_map_polyline_elements())

    def test_marker_has_popup_with_individual_name_and_timestamp_when_clicked(self):
        self.page.change_individual_selection(str(self.I.id))
        self.page.get_marker().click()
        self.assert_popup_contents()

    def test_marker_has_popup_with_individual_name_and_timestamp_when_clicked_and_playing(self):
        self.select_individual_and_play()
        self.page.get_marker().click()
        self.assert_popup_contents()

    def assert_popup_contents(self):
        popuptext = self.page.get_popup().get_attribute("innerHTML")
        self.assertEquals("Birdie" in popuptext, True)
        self.assertEquals("2010" in popuptext, True)

    def select_individual_and_play(self):
        self.page.change_individual_selection(str(self.I.id))
        while self.page.driver.find_element_by_id("loading").is_displayed():
            time.sleep(1)
        self.page.play()

    def test_slider_label_value_changes_when_playing(self):
        self.select_individual_and_play()
        label = self.page.driver.find_element_by_id("playLabel")
        self.assertNotEquals(label.get_attribute("innerHTML"), "1234/12/12 12:12:12")

    def test_polyline_is_drawn_when_playing(self):
        self.select_individual_and_play()
        startcount = len(self.page.driver.find_elements_by_tag_name("g"))
        time.sleep(1)
        self.assertGreater(len(self.page.driver.find_elements_by_tag_name("g")), startcount)

    def test_navigation_is_shown_if_logged_in(self):
        self.page.navigate()

        try:
            self.page.get_navigation()
        except:
            self.fail()

    def test_navigation_is_not_shown_if_not_logged_in(self):
        settings.MOCK_AUTHENTICATION = 'On'
        self.page.navigate()

        try:
            self.page.get_navigation()
            self.fail()
        except:
            pass
        finally:
            settings.MOCK_AUTHENTICATION = "Skip"

    def test_speed_sets_with_param(self):
        self.assertEquals('75', self.page.get_speed_set_as_param(75))

    def test_iframe_url_is_correct(self):
        self.page.change_individual_selection(str(self.I.id))
        self.assertEquals(
            'http://127.0.0.1/papukaani/public/?lang={lang}&individuals=[{individual}]&speed={speed}&zoom={zoom}&loc={loc}'.format(
                lang=self.lang, individual=str(self.I.id), speed=250, zoom=4, loc='[61.01,68.01]'),
            self.page.get_iframe_url())

    def test_iframe_url_is_correct_if_url_parameters_have_been_given(self):
        self.page.driver.get(self.page.url + "?zoom=6&loc=[20,40]")
        self.page.change_individual_selection(str(self.I.id))
        self.assertEquals(
            'http://127.0.0.1/papukaani/public/?lang={lang}&individuals=[{individual}]&speed={speed}&zoom={zoom}&loc={loc}'.format(
                lang=self.lang, individual=str(self.I.id), speed=250, zoom=4, loc='[61.01,68.01]'),
            self.page.get_iframe_url())

    def test_iframe_url_is_correct_if_url_parameters_are_invalid(self):
        self.page.driver.get(self.page.url + "?zoom=5&loc=5")
        self.page.change_individual_selection(str(self.I.id))
        self.assertEquals(
            'http://127.0.0.1/papukaani/public/?lang={lang}&individuals=[{individual}]&speed={speed}&zoom={zoom}&loc={loc}'.format(
                lang=self.lang, individual=str(self.I.id), speed=250, zoom=4, loc='[61.01,68.01]'),
            self.page.get_iframe_url())

    def test_animation_initially_forwards_to_end_so_whole_path_can_be_seen(self):
        number_of_polylines = 71
        self.page.change_individual_selection(str(self.I.id))
        self.assertEquals(len(self.page.driver.find_elements_by_tag_name("g")), number_of_polylines)

    def test_animation_initially_forwards_to_end_so_whole_path_can_be_seen_with_two_birds(self):
        self.page.change_individual_selection(str(self.I2.id))
        self.page.change_individual_selection(str(self.I.id))
        self.assertEquals(len(self.page.driver.find_elements_by_tag_name("g")), 73)

    def test_speedslider_is_hidden_initially(self):
        self.assertEquals(self.page.SPEED_SLIDER.is_displayed(), False)

    def test_speedslider_is_shown_on_mouse_hover(self):
        ActionChains(self.page.driver).move_to_element(self.page.SPEED_SLIDER_LABEL).perform()
        time.sleep(1)
        self.assertEquals(self.page.SPEED_SLIDER.is_displayed(), True)

    def test_speedslider_tooltip_can_be_seen_on_mouse_hover(self):
        ActionChains(self.page.driver).move_to_element(self.page.SPEED_SLIDER_LABEL).perform()
        time.sleep(1)
        ActionChains(self.page.driver).move_to_element(self.page.SPEED_SLIDER).perform()
        time.sleep(1)
        self.assertEquals(self.page.SPEED_SLIDER.get_attribute("aria-describedby"), "ui-id-1")

    def test_time_selection_shows_correct_points(self):
        self.page.TIME_START.send_keys("10.12.2010 00:00")
        self.page.TIME_END.send_keys("14.12.2010 00:00")
        # just to defocus (blur) previous field
        self.page.TIME_END.send_keys(Keys.ENTER)
        time.sleep(1)
        self.page.change_individual_selection(str(self.I.id))
        self.assertTrue("10.12.2010" in self.page.driver.find_element_by_id("playLabel").text)
        self.assertTrue("14.12.2010" in self.page.driver.find_element_by_id("playLabel_end").text)

    def test_time_selection_refresh_works(self):
        self.page.change_individual_selection(str(self.I.id))
        time.sleep(2)
        self.page.TIME_START.send_keys("10.12.2010 00:00")
        self.page.TIME_END.send_keys("14.12.2010 00:00")
        # just to defocus (blur) previous field
        self.page.TIME_END.send_keys(Keys.ENTER)
        time.sleep(1)
        self.assertTrue("10.12.2010" in self.page.driver.find_element_by_id("playLabel").text)
        self.assertTrue("14.12.2010" in self.page.driver.find_element_by_id("playLabel_end").text)

    def test_iframe_with_time_selection_is_correct(self):
        self.page.change_individual_selection(str(self.I.id))
        self.assertEquals(
            'http://127.0.0.1/papukaani/public/?lang={lang}&individuals=[{individual}]&speed={speed}&zoom={zoom}&loc={loc}'.format(
                lang=self.lang, individual=str(self.I.id), speed=250, zoom=4, loc='[61.01,68.01]'),
            self.page.get_iframe_url())

        self.page.TIME_START.send_keys("11.12.2010 00:00")
        time.sleep(3)
        self.assertEquals(
            'http://127.0.0.1/papukaani/public/?lang={lang}&individuals=[{individual}]&speed={speed}&zoom={zoom}&loc={loc}&start_time={start_time}'.format(
                lang=self.lang, individual=str(self.I.id), speed=250, zoom=4, loc='[61.01,68.01]',
                start_time='11.12.2010 00:00'),
            self.page.get_iframe_url())

        self.page.TIME_END.send_keys("14.12.2010 00:00")
        time.sleep(3)
        self.assertEquals(
            'http://127.0.0.1/papukaani/public/?lang={lang}&individuals=[{individual}]&speed={speed}&zoom={zoom}&loc={loc}&start_time={start_time}&end_time={end_time}'.format(
                lang=self.lang, individual=str(self.I.id), speed=250, zoom=4, loc='[61.01,68.01]',
                start_time='11.12.2010 00:00', end_time='14.12.2010 00:00'),
            self.page.get_iframe_url())

    def test_time_selection_in_get_parameters_show_correct_time_selection(self):
        self.page.driver.get(self.page.url + "?start_time=11.12.2010 00:00&end_time=14.12.2010 00:00")

        self.assertEquals(self.page.TIME_START.get_attribute("value"), "11.12.2010 00:00")
        self.assertEquals(self.page.TIME_END.get_attribute("value"), "14.12.2010 00:00")

    def test_description_button_opens_modal_with_correct_info(self):
        self.page.change_individual_selection(str(self.I.id))
        self.page.driver.find_element_by_css_selector(
            "#individual" + str(self.I.id) + " button.showDescription").click()
        time.sleep(1)
        self.assertTrue(
            self.page.driver.find_element_by_css_selector("#descriptionModal h4.modal-title").text == ("Birdie"))

        self.assertTrue(
            self.page.driver.find_element_by_css_selector("#descriptionModal h6.modal-species").text == ("Kaakkuri"))
        self.assertEquals(self.page.driver.find_element_by_id("desc").text, "birdiekuvaus")
        self.assertTrue(
            self.page.driver.find_element_by_id("url").get_attribute("href") == ("http://www.birdie.kek/"))

    def test_description_button_missing_when_no_desc_or_url_available(self):
        self.page.change_individual_selection(str(self.I2.id))
        with self.assertRaises(NoSuchElementException):
            self.page.driver.find_element_by_css_selector("#individual" + str(self.I2.id) + " button.showDescription")

    def test_canvas_displays_initially(self):  # empty
        self.assertEqual(self.canvas['empty'], self.page.get_linelayercanvas_as_base64())

    def test_canvas_displays_empty_after_remove_all(self):  # empty
        self.page.change_individual_selection(str(self.I.id))
        self.page.remove_selected_individual(str(self.I.id))
        self.assertEqual(self.canvas['empty'], self.page.get_linelayercanvas_as_base64())

    def test_canvas_displays_one_path(self):  # one red line
        self.page.change_individual_selection(str(self.I.id))
        self.assertEqual(self.canvas['long-red'], self.page.get_linelayercanvas_as_base64())

    def test_canvas_displays_one_path2(self):  # one red line
        self.page.change_individual_selection(str(self.I2.id))
        self.assertEqual(self.canvas['long-red'], self.page.get_linelayercanvas_as_base64())

    def test_canvas_displays_two_paths(self):  # long red, narrow blue
        self.page.change_individual_selection(str(self.I.id))
        self.page.change_individual_selection(str(self.I2.id))
        self.assertEqual(self.canvas['long-red-narrow-blue'], self.page.get_linelayercanvas_as_base64())

    def test_canvas_displays_one_path_after_two_additions_and_former_removed(self):  # long blue
        self.page.change_individual_selection(str(self.I.id))
        self.page.change_individual_selection(str(self.I2.id))
        self.page.remove_selected_individual(str(self.I.id))
        self.assertEqual(self.canvas['long-blue'], self.page.get_linelayercanvas_as_base64())

    def test_canvas_displays_one_path_after_two_additions_and_time_change(self):  # one red line
        self.page.change_individual_selection(str(self.I.id))
        self.page.change_individual_selection(str(self.I2.id))
        self.page.TIME_START.send_keys("13.12.2010 00:00")
        self.page.TIME_START.send_keys(Keys.ENTER)
        self.assertEqual(self.canvas['long-red'], self.page.get_linelayercanvas_as_base64())