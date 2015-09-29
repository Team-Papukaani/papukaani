from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from selenium import webdriver
from papukaani.settings import *
import time


class FileUploadSeleniumTest(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.c = Client()

    def tearDown(self):
        self.browser.close()

    def test_selenium_file_can_be_uploaded_and_points_will_be_shown_on_map(self):
        base_url = 'http://127.0.0.1:8081'
        self.browser.get(base_url + '/papukaani/upload')
        upload = self.browser.find_element_by_name("file")
        upload.send_keys(BASE_DIR + "/papukaaniApp/tests/test_files/ecotones.csv")
        upload.submit()
        time.sleep(1)
        self.assertTrue("Tiedostosi formaatti ei ole kelvollinen" not in self.browser.page_source)
        self.assertTrue("Et valinnut ladattavaa tiedostoa" not in self.browser.page_source)
        self.assertTrue(len(self.browser.find_elements_by_tag_name("g")) == 1)
