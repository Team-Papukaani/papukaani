from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client

from papukaaniApp.tests.page_models.page_models import PublicPage
from django.conf import settings
from papukaaniApp.models_LajiStore import *


class PublicView(StaticLiveServerTestCase):

    def setUp(self):
        self.device_id = "DeviceId"
        self.A = document.create("TestA", [gathering.Gathering("1234-12-12T12:12:12+00:00", [61.0, 23.0], publicity="public"), gathering.Gathering("1234-12-12T12:12:12+00:00", [61.01, 23.01], publicity="private")], self.device_id)

    def tearDown(self):
        self.A.delete()

    def test_some_points_are_shown_on_map(self):

        public = PublicPage(self.device_id)
        public.navigate()

        self.assertGreater(public.get_points_json().count('['), 0)

        public.close()
