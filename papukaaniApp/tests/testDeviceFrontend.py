from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import DevicePage
from selenium.common.exceptions import NoSuchElementException

_filePath = "papukaaniApp/tests/test_files/"


class TestDeviceFrontend(StaticLiveServerTestCase):
    def setUp(self):
        dev = {
            "deviceId": "DeviceId",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "createdAt": "2015-09-29T14:00:00+03:00",
            "lastModifiedAt": "2015-09-29T14:00:00+03:00",
            "facts": []
        }
        self.D = device.create(**dev)

        self.I = individual.create("12345TESTINDIVIDUAL", "Birdie")
        self.D.attach_to(self.I, "2015-11-02T14:00:00+02:00")

        self.D.update()

        self.page = DevicePage()
        self.page.navigate()

        self.page.change_device_selection("DeviceId")
        self.page.find_controls()

    def tearDown(self):
        self.D.delete()
        self.I.delete()
        self.page.close()
        document.delete_all()

    def test_individual_info_visible(self):
        self.assertEquals("Birdie", self.page.get_individual_name("12345TESTINDIVIDUAL"))

    def test_only_currently_attached_bird_has_remove_button(self):
        self.assertEquals(1, len(self.page.driver.find_elements_by_class_name("btn-danger")))

    def test_if_unremoved_birds_attach_button_is_not_visible(self):
        self.assertFalse(self.page.ATTACHER.is_displayed())

        self.page.REMOVE_TIME.send_keys("03-11-2015 00:00")
        self.page.REMOVE.click()

        self.assertTrue(self.page.ATTACHER.is_displayed())

    def test_removed_individuals_are_not_selectable(self):
        self.I.deleted = True
        self.I.update()
        with self.assertRaises(NoSuchElementException):
            self.page.attach_individual("Birdie", "12-11-2015 00:00")

    def test_attacher_is_hidden_after_attach(self):
        self.page.REMOVE_TIME.send_keys("03-11-2015 00:00")
        self.page.REMOVE.click()

        self.page.attach_individual("12345TESTINDIVIDUAL", "12-11-2015 00:00")

        self.assertFalse(self.page.ATTACHER.is_displayed())

    def test_attacher_is_shown_after_remove(self):
        self.detach_and_assert("03-11-2015 00:00", True)

    def test_cant_remove_if_remove_time_is_before_attach_time(self):
        self.detach_and_assert("01-10-2015 02:00", False)

    def test_cant_remove_if_remove_time_is_in_the_future(self):
        self.detach_and_assert("13-12-2114 00:00", False)

    def test_can_remove_when_all_conditions_are_met(self):
        self.detach_and_assert("03-11-2015 14:00", True)

    def test_cant_attach_if_start_time_is_in_future(self):
        self.page.REMOVE_TIME.send_keys("03-11-2015 14:00")
        self.page.REMOVE.click()

        self.page.attach_individual("12345TESTINDIVIDUAL", "13-12-2114 00:00")

        self.assertTrue(self.page.ATTACHER.is_displayed())

    def test_cant_attach_if_start_time_overlaps_with_another_device(self):
        self.page.REMOVE_TIME.send_keys("03-11-2015 14:00")
        self.page.REMOVE.click()

        self.page.attach_individual("12345TESTINDIVIDUAL", "02-11-2015 16:00")

        self.assertTrue(self.page.ATTACHER.is_displayed())

    def test_can_attach_id_all_conditions_are_met(self):
        self.page.REMOVE_TIME.send_keys("03-11-2015 14:00")
        self.page.REMOVE.click()

        self.page.attach_individual("12345TESTINDIVIDUAL", "04-11-2015 16:00")

        self.assertFalse(self.page.ATTACHER.is_displayed())

    def test_errors_messages_are_shown_when_validation_fails(self):
        self.page.REMOVE_TIME.send_keys("03-11-2015 14:00")
        self.page.REMOVE.click()

        self.page.attach_individual("12345TESTINDIVIDUAL", "13-12-2114 00:00")

        self.assertTrue(len(self.page.driver.find_element_by_id("errors").text) > 0)

    def test_cant_attach_if_time_field_is_empty(self):
        self.page.REMOVE_TIME.send_keys("03-11-2015 14:00")
        self.page.REMOVE.click()

        self.page.ATTACH.click()

        self.assertTrue(self.page.ATTACHER.is_displayed())

    def test_cant_remove_if_time_field_is_empty(self):
        self.page.REMOVE.click()

        self.assertFalse(self.page.ATTACHER.is_displayed())

    def detach_and_assert(self, time, result):
        self.page.REMOVE_TIME.send_keys(time)
        self.page.REMOVE.click()

        self.assertEquals(self.page.ATTACHER.is_displayed(), result)
