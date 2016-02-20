from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from papukaaniApp.tests.page_models.page_models import NavigationPage, UploadPage
from papukaaniApp.tests.page_models.page_model import Page

class TestLanguage(StaticLiveServerTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_default_finnish(self):
        nav = NavigationPage()
        nav.navigate()
        ul_text = nav.driver.find_element_by_id('upload_link').text
        self.assertEquals(ul_text.lower().strip(), 'lataa tiedosto')
        nav.close()

    def test_link_name_changes(self):
        nav = NavigationPage()
        nav.navigate()
        nav.driver.find_element_by_id('language_en').click()
        ul_text = nav.driver.find_element_by_id('upload_link').text
        self.assertEquals(ul_text.lower().strip(), 'upload file')
        nav.close()

    def test_selection_persists(self):
        page = Page()
        page.url = NavigationPage.url
        page.navigate()

        page.driver.find_element_by_id('language_en').click()

        page.url = UploadPage.url
        page.navigate()
        ul_text = page.driver.find_element_by_id('upload_link').text
        self.assertEquals(ul_text.lower().strip(), 'upload file')
        page.close()
