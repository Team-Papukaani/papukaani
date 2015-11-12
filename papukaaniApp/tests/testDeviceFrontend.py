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
        self.D.attach_to(self.I, "2015-11-02T14:00:00+03:00")
        self.D.update()

        self.page = DevicePage()
        self.page.navigate()

        self.page.change_device_selection("DeviceId")

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
        self.assertFalse(self.page.driver.find_element_by_id("attacher").is_displayed())

        self.page.driver.find_element_by_id("remove_time").send_keys("2015-11-02T14:00:00+03:00")
        self.page.driver.find_element_by_class_name("btn-danger").click()

        self.assertTrue(self.page.driver.find_element_by_id("attacher").is_displayed())

    def test_attach_button_is_disabled_after_attach(self):
        self.page.driver.find_element_by_id("remove_time").send_keys("2015-11-02T14:00:00+03:00")
        self.page.driver.find_element_by_class_name("btn-danger").click()

        self.page.driver.find_element_by_id("attach").send_keys("2015-11-02T14:00:00+03:00")
        self.page.driver.find_element_by_id("attach").click()

    def test_removed_individuals_are_not_selectable(self):
        self.I.deleted = True
        self.I.update()
        with self.assertRaises(NoSuchElementException):
            self.page.attach_individual("Birdie")
