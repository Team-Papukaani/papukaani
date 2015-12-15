from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import IndividualPage

class TestIndividualFrontend(StaticLiveServerTestCase):
    def setUp(self):
        self.I = individual.create("ERIEUR")
        self.page = IndividualPage()
        self.page.navigate()

    def tearDown(self):
        self.I.delete()
        self.page.close()
        individual.delete_all()

    def test_individual_info_visible(self):
        self.assertEquals("ERIEUR", self.page.get_first_individual_taxon())

    def test_modify_individual(self):
        self.page.modify_individual("GAVARC", "DEM123456")
        self.assertEquals("GAVARC", self.page.get_first_individual_nickname())
        self.assertEquals("DEM123456", self.page.get_first_individual_ring_id())

    def test_delete_and_create_individual(self):
        self.page.delete_individual()
        self.page.create_new_individual("PODCRI", "Sockbird")
        self.assertEquals("PODCRI", self.page.get_first_individual_taxon())
        self.assertEquals("Sockbird", self.page.get_first_individual_nickname())
