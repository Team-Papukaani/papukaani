from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client

from papukaaniApp.tests.page_models.page_models import PublicPage
from django.conf import settings
from papukaaniApp.models_LajiStore import *


class PublicView(StaticLiveServerTestCase):

    def setUp(self):
        self.A = document.create("TestA", [gathering.Gathering("1234-12-12T12:12:12+00:00", [61.0, 23.0], publicity="public"), gathering.Gathering("1234-12-12T12:12:12+00:00", [61.01, 23.01], publicity="private")], "DeviceId")
        self.page = public = PublicPage()
        self.page.navigate()

    def tearDown(self):
        self.page.close()
        self.A.delete()

    def test_some_points_are_shown_on_map(self):
        self.assertGreater(self.page.get_number_of_points(), 0)

    def test_can_choose_points_by_device(self):
        B = document.create("TestB", [], 'DeviceId2')
        self.page.navigate()

        self.assertGreater(self.page.get_number_of_points(), 0)
        self.page.change_device_selection("DeviceId2")

        self.assertEquals(self.page.get_number_of_points(), 0)
        B.delete()


