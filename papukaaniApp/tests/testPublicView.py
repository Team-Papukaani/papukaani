from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.test import Client

from papukaaniApp.tests.page_models.page_models import PublicPage
from papukaani.config.common import *
from papukaaniApp.models import MapPoint


class PublicView(StaticLiveServerTestCase):

    def test_public_points_are_shown_on_map(self):
        with open(BASE_DIR + "/papukaaniApp/tests/test_files/ecotones.csv") as file:
            Client().post('/papukaani/upload/', {'file': file})

        points = MapPoint.objects.all()
        len(points)

        for num in range(1, 5):
            points[num].public = 1
            points[num].save()

        public = PublicPage(points[1].creature.id)
        public.navigate()

        self.assertEquals(public.get_points_json().count('['), 5)  # 4 JSON points + 1 for the containing array
        self.assertNotEquals(public.get_map_polyline_elements(), None)  # <g> includes polylines on map
        public.close()
