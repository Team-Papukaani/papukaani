from time import sleep
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from papukaaniApp.models import GeneralParser
from papukaaniApp.tests.test_data import create_jouko_parser
from papukaaniApp.tests.page_models.page_models import FormatPage, FormatListPage


class TestFormatFrontend(StaticLiveServerTestCase):

    def setUp(self):
        self.page = FormatPage()
        self.page.navigate()
        GeneralParser.objects.all().delete()
        self.list_page = FormatListPage()

    def tearDown(self):
        self.page.close()
        self.list_page.close()
        GeneralParser.objects.all().delete()

    def test_info_boxes_are_hidden(self):
        self.assertFalse(self.page.HELP_BOX.is_displayed())

    def test_info_box_is_shown_when_info_button_is_clicked(self):
        self.page.HELP_BUTTON.click()

        self.assertTrue(self.page.HELP_BOX.is_displayed())

    def test_info_box_is_hidden_when_info_button_is_clicked_again(self):
        self.page.HELP_BUTTON.click()
        self.page.HELP_BUTTON.click()

        self.assertFalse(self.page.HELP_BOX.is_displayed())

    def test_create_format(self):
        self.page.input_values_and_submit("Eco","TS", "Date", "Time", "Lon", "Lat", "gps", "temp", "alt")
        self.assertEquals(len(GeneralParser.objects.all()), 1)

    def test_input_validation(self):
        self.assertEquals(len(GeneralParser.objects.all()), 0)
        self.page.input_values_and_submit("Eco","", "", "Time", "Lon", "Lat", "gps", "temp", "alt")
        self.assertEquals(len(GeneralParser.objects.all()), 0)


class TestFormatListFrontend(StaticLiveServerTestCase):

    def setUp(self):
        GeneralParser.objects.all().delete()
        create_jouko_parser()
        self.page = FormatListPage()
        self.page.navigate()

    def tearDown(self):
        self.page.close()
        GeneralParser.objects.all().delete()

    def test_format_shows_in_the_list_page(self):
        self.assertTrue(self.page.does_page_contain("jouko"))

    def test_delete_format_in_the_list_page(self):
        self.page.delete_first_format()
        self.assertFalse(self.page.does_page_contain("jouko"))