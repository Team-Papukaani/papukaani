from time import sleep
from django.conf.urls import url
from django.core.urlresolvers import reverse
from django.test.testcases import LiveServerTestCase

from selenium import webdriver

from papukaaniApp.tests.page_models import MainNavigation
from papukaaniApp.views.upload_views import upload


class TestNavigation(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.PhantomJS()
        self.base_url = 'http://127.0.0.1:8081'
        self.browser.get(self.base_url + '/papukaani')

    def test(self):
        MainNavigation(self.browser).open_upload_page()
        sleep(5)
        self.assertEquals(self.browser.current_url, self.base_url + reverse("upload"))
        self.browser.close()


