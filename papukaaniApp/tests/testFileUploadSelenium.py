from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver

from papukaani.settings import *
from papukaaniApp.tests.page_models.page_models import UploadPage


class FileUploadSeleniumTest(StaticLiveServerTestCase):
    def setUp(self):
        self.driver = webdriver.PhantomJS()
        self.upload = UploadPage(self.driver)
        self.upload.navigate()

    def tearDown(self):
        self.driver.close()

    def test_selenium_file_can_be_uploaded_and_points_will_be_shown_on_map(self):
        self.upload.upload_file(BASE_DIR + "/papukaaniApp/tests/test_files/ecotones.csv")
        self.assertNotEquals("Tiedostosi formaatti ei ole kelvollinen", self.upload.get_message())
        self.assertNotEquals("Et valinnut ladattavaa tiedostoa", self.upload.get_message())
        self.assertNotEquals(self.upload.get_map_polyline_elements(), None)
