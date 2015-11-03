from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import DevicePage

_filePath = "papukaaniApp/tests/test_files/"


class TestDeviceFrontend(StaticLiveServerTestCase):
    def setUp(self):
        #self.A = device.create('1234TEST_A','type','manufact','2015-10-27T16:32:01+00:00', '2015-10-27T16:32:01+00:00', [])
        dev = {
            "deviceId": "DeviceId",
            "deviceType": "Type",
            "deviceManufacturer": "Manufacturer",
            "createdAt": "2015-09-29T14:00:00+03:00",
            "lastModifiedAt": "2015-09-29T14:00:00+03:00",
            "facts": []
        }
        self.D = device.create(**dev)
        self.I = individual.create("12345TESTINDIVIDUAL","Birdie")
        self.D.attach_to(self.I, "2015-11-02T14:00:00+03:00")
        self.D.update()

        self.page = DevicePage()
        self.page.navigate()

        self.page.change_device_selection("DeviceId")

    def tearDown(self):
        #self.A.delete()
        self.D.delete()
        self.I.delete()
        self.page.close()
        document.delete_all()

    def test_individual_info_visible(self):
        self.assertEquals("Birdie", self.page.get_individual_name("12345TESTINDIVIDUAL"))

    # def test_cluster_with_only_public_points_is_green(self):
    #     self.page.double_click_marker()
    #     self.assertEquals(1, self.page.number_of_completely_public_clusters_on_map())
    #     self.assertEquals(0, self.page.number_of_private_clusters_on_map())
    #     self.assertEquals(0, self.page.number_of_partially_public_clusters_on_map())

        """
        - lintu löytyy listasta
        - lähetin löytyy listasta
        - lähettimellä näkyy lintu formatoituna
        """

