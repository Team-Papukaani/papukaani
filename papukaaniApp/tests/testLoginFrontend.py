import time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from pyvirtualdisplay import Display
from papukaaniApp.tests.test_utils import *
from selenium import webdriver

from django.conf import settings

class TestLoginFrontend(StaticLiveServerTestCase):

    BASE_URL = "http://127.0.0.1:8081"

    def setUp(self):
        settings.MOCK_AUTHENTICATION = "On"
        self.display = Display(visible=settings.XEPHYR_VISIBILITY, size=(1920,1400))
        self.display.start()
        self.driver = get_configured_firefox()

        self.choose_page = self.BASE_URL + '/papukaani/choose'
        self.index_page = self.BASE_URL + '/papukaani'
        self.logout_page = self.BASE_URL + '/papukaani/logout'
        self.login_page = self.BASE_URL + '/papukaani/login'

    def tearDown(self):
        take_screenshot_of_test_case(self, self.driver)
        self.driver.get(self.logout_page)
        settings.MOCK_AUTHENTICATION = "Skip"
        self.driver.close()
        self.display.stop()

    def test_choose_redirects_to_login_if_not_logged_in(self):
        self.driver.get(self.choose_page)
        try:
            self.driver.find_element_by_id("map")
            self.fail()
        except:
            pass

    def test_choose_does_not_redirect_if_logged_in(self):
        self.driver.get(self.login_page)
        self.driver.find_element_by_id("choose_link").click()
        time.sleep(2)
        try:
            self.driver.find_element_by_id("map")
        except:
            self.fail()

    def test_login_link_is_shown_if_not_logged_int(self):
        self.driver.get(self.index_page)
        try:
            self.driver.find_element_by_id("login_link")
        except:
            self.fail()

    def test_logout_link_is_shown_if_logged_in(self):
        self.driver.get(self.login_page)
        try:
            self.driver.find_element_by_id("logout_link")
        except:
            self.fail()

    def test_login_link_is_not_shown_if_logged_in(self):
        self.driver.get(self.login_page)
        try:
            self.driver.find_element_by_id("login_link")
            self.fail()
        except:
            pass

    def test_logout_link_is_not_shown_if_not_logged_in(self):
        self.driver.get(self.index_page)
        try:
            self.driver.find_element_by_id("logout_link")
            self.fail()
        except:
            pass
