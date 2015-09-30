from django.test.testcases import LiveServerTestCase
from selenium import webdriver

from papukaaniApp.tests.page_models.page_models import NavigationPage


class TestNavigation(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.PhantomJS()

    def tearDown(self):
        self.browser.close()

    def test(self):
        nav = NavigationPage(self.browser)
        nav.navigate()
        nav.open_upload_page()
        self.assertEquals(str(self.browser.current_url), str(nav.url) + 'upload/')
