from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client
from selenium import webdriver
from papukaani.settings import *
from papukaaniApp.models import MapPoint


class PublicView(StaticLiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.c = Client()

    def tearDown(self):
        self.browser.close()

    def test_public_points_are_shown_on_map(self):
        with open(BASE_DIR + "/papukaaniApp/tests/test_files/ecotones.csv") as file:
            self.c.post('/papukaani/upload/', {'file': file})

        points = MapPoint.objects.all()
        len(points)
        for num in range(1, 5):
            points[num].public = 1
            points[num].save()

        base_url = 'http://127.0.0.1:8081'
        self.browser.get(base_url + '/papukaani/public/1')
        json_points = self.browser.find_element_by_id("mapScript").get_attribute("innerHTML")

        self.assertTrue(json_points.count('[') == 5)  # 4 JSON points + 1 for the containing array
        self.assertTrue(len(self.browser.find_elements_by_tag_name("g")) == 1)  # <g> includes polylines on map
