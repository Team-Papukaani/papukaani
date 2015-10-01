from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from papukaaniApp.tests.page_models.page_models import NavigationPage


class TestNavigation(StaticLiveServerTestCase):
    def setUp(self):
        self.nav = NavigationPage()
        self.nav.navigate()

    def tearDown(self):
        self.nav.close()

    def test(self):
        self.nav.open_upload_page()
        self.assertEquals(str(self.nav.driver.current_url), str(self.nav.url) + 'upload/')
