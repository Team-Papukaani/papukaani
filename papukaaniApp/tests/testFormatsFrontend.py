from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from papukaaniApp.tests.test_utils import take_screenshot_of_test_case
from papukaaniApp.tests.page_models.page_models import FormatsPage

class TestFormatsFrontend(StaticLiveServerTestCase):

    def setUp(self):
        self.page = FormatsPage()
        self.page.navigate()

    def tearDown(self):
        self.page.close()

    def test_info_boxes_are_hidden(self):
        self.assertFalse(self.page.HELP_BOX.is_displayed())

    def test_info_box_is_shown_when_info_button_is_clicked(self):
        self.page.HELP_BUTTON.click()

        self.assertTrue(self.page.HELP_BOX.is_displayed())

    def test_info_box_is_hidden_when_info_button_is_clicked_again(self):
        self.page.HELP_BUTTON.click()
        self.page.HELP_BUTTON.click()

        self.assertFalse(self.page.HELP_BOX.is_displayed())