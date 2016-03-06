from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from papukaaniApp.tests.page_models.page_models import NavigationPage
from papukaaniApp.tests.test_utils import take_screenshot_of_test_case


class TestNavigation(StaticLiveServerTestCase):
    def setUp(self):
        self.nav = NavigationPage()
        self.nav.navigate()

    def tearDown(self):
        take_screenshot_of_test_case(self, self.nav.driver)
        self.nav.close()

#    def test(self):
#        self.nav.open_upload_page()
#        self.assertEquals(str(self.nav.driver.current_url), str(self.nav.url) + 'upload/')
