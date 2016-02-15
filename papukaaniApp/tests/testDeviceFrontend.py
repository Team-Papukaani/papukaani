from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import DevicePage
from papukaaniApp.services.deviceindividual_service import DeviceIndividual
import time

_filePath = "papukaaniApp/tests/test_files/"


class TestDeviceFrontend(StaticLiveServerTestCase):
    def setUp(self):
        dev = {
            "deviceManufacturerID": "DeviceId",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "dateCreated": "2015-09-29T14:00:00+03:00",
            "dateEdited": "2015-09-29T14:00:00+03:00"
        }
        self.D = device.create(**dev)

        self.I = individual.create("NICK","Birdie")

        self.D.attach_to(self.I.id, "2015-11-02T14:00:00+02:00")

        self.page = DevicePage()
        self.page.navigate()

        self.page.change_device_selection(str(self.D.id))

    def tearDown(self):
        time.sleep(3) # previous test conflicts with the next one and results in stacktrace because of "null-pointers"
        device.delete_all()
        individual.delete_all()
        document.delete_all()
        DeviceIndividual.delete_all()
        self.page.close()

    def test_individual_info_visible(self):
        self.assertEquals(self.I.nickname, self.page.get_individual_name(self.I.id))

    def test_only_currently_attached_bird_has_remove_button(self):
        self.assertEquals(1, len(self.page.driver.find_elements_by_class_name("btn-danger")))

    def test_if_unremoved_birds_attach_button_is_not_visible(self):
        self.assertFalse(self.page.ATTACHER.is_displayed())

        self.page.REMOVE_TIME.send_keys("03.11.2015 00:00")
        self.page.REMOVE.click()

        self.assertTrue(self.page.ATTACHER.is_displayed())

    def test_attacher_is_hidden_after_attach(self):
        self.page.REMOVE_TIME.send_keys("03.11.2015 00:00")
        self.page.REMOVE.click()

        self.page.attach_individual(str(self.I.id), "12.11.2015 00:00")

        self.assertFalse(self.page.ATTACHER.is_displayed())

    def test_attacher_is_shown_after_remove(self):
        self.detach_and_assert("03.11.2015 00:00", True)

    def test_cant_remove_if_remove_time_is_before_attach_time(self):
        self.detach_and_assert("01.10.2015 02:00", False)

    def test_cant_remove_if_remove_time_is_in_the_future(self):
        self.detach_and_assert("13.12.2114 00:00", False)

    def test_can_remove_when_all_conditions_are_met(self):
        self.detach_and_assert("03.11.2015 14:00", True)

    def test_cant_attach_if_start_time_is_in_future(self):
        self.detach_and_attach_and_assert("03.11.2015 14:00", str(self.I.id), "13.12.2114 00:00", True)

    def test_cant_attach_if_start_time_overlaps_with_another_device(self):
        self.detach_and_attach_and_assert("03.11.2015 14:00", str(self.I.id), "02.11.2015 16:00", True)

    def test_can_attach_if_all_conditions_are_met(self):
        self.detach_and_attach_and_assert("03.11.2015 14:00", str(self.I.id), "04.11.2015 16:00", False)

    def test_errors_messages_are_shown_when_validation_fails(self):
        self.page.REMOVE_TIME.send_keys("03.11.2015 14:00")
        self.page.REMOVE.click()

        self.assertTrue(len(self.page.driver.find_element_by_id("errors").text) > 0)

    def test_cant_attach_if_time_field_is_empty(self):
        self.page.REMOVE_TIME.send_keys("03.11.2015 14:00")
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

    def detach_and_attach_and_assert(self, timedetached, individualid, timeattached, result):
        self.page.REMOVE_TIME.send_keys(timedetached)
        self.page.REMOVE.click()

        self.page.attach_individual(individualid, timeattached)

        self.assertEquals(self.page.ATTACHER.is_displayed(), result)
