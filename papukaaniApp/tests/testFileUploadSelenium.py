from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from django.conf import settings
from papukaaniApp.tests.page_models.page_models import UploadPage
from papukaaniApp.tests.test_utils import take_screenshot_of_test_case
from papukaaniApp.models import *


class FileUploadSeleniumTest(StaticLiveServerTestCase):
    def setUp(self):
        self.ecotone_parser = GeneralParser.objects.create(formatName="ecotone", gpsNumber="GpsNumber",
                                                           timestamp="GPSTime",
                                                           longitude="Longtitude", latitude="Latitude",
                                                           altitude="Altitude",
                                                           temperature="Temperature")
        self.ecotone_parser.save()
        self.upload = UploadPage()
        self.upload.navigate()

    def tearDown(self):
        self.ecotone_parser.delete()
        take_screenshot_of_test_case(self, self.upload.driver)
        self.upload.close()

    def test_selenium_file_can_be_uploaded_and_points_will_be_shown_on_map(self):
        self.upload.change_format_selection("ecotone")
        self.upload.upload_file(settings.BASE_DIR + "/papukaaniApp/tests/test_files/ecotones.csv")
        self.assertNotEquals("Tiedostosi formaatti ei ole kelvollinen", self.upload.get_message().strip())
        self.assertNotEquals("Et valinnut ladattavaa tiedostoa", self.upload.get_message().strip())
        self.assertEquals("Tiedoston lataus onnistui!", self.upload.get_message().strip())
        self.assertNotEquals(self.upload.get_map_polyline_elements(), None)

    def test_correct_error_message_if_no_file_selected(self):
        self.upload.change_format_selection("ecotone")
        self.upload.push_upload_button()
        self.assertEquals("Et valinnut ladattavaa tiedostoa!", self.upload.get_message().strip())

    def test_correct_error_message_if_invalid_file_format(self):
        self.upload.change_format_selection("ecotone")
        self.upload.upload_file(settings.BASE_DIR + "/papukaaniApp/tests/test_files/invalid.txt")
        self.assertEquals("Tiedostosi formaatti ei ole kelvollinen!", self.upload.get_message().strip())
