from django.test.testcases import LiveServerTestCase
from selenium import webdriver

from papukaaniApp.tests.page_models.page_models import NavigationPage


class TestNavigation(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.nav = NavigationPage(self.browser)
        self.nav.navigate()

    def tearDown(self):
        self.browser.close()

    def test(self):
        self.nav.open_upload_page()
        self.assertEquals(str(self.browser.current_url), str(self.nav.url) + 'upload/')
