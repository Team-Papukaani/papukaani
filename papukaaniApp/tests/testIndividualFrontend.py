from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from papukaaniApp.models_LajiStore import *
from papukaaniApp.tests.page_models.page_models import IndividualPage

class TestIndividualFrontend(StaticLiveServerTestCase):
    def setUp(self):
        self.I = individual.create("12345TESTINDIVIDUAL","ERIEUR")
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

    def test_correct_message_if_no_name_and_no_taxon(self):
        self.page.create_new_individual("", "")
        self.assertEquals("Laji puuttuu!", self.page.get_message().strip())

    def test_correct_message_if_no_name(self):
        self.page.create_new_individual("Kuikka", "")
        self.assertEquals("Nimi puuttuu!", self.page.get_message().strip())

    def test_correct_message_if_no_taxon(self):
        self.page.create_new_individual("", "Seppo")
        self.assertEquals("Laji puuttuu!", self.page.get_message().strip())

    def test_correct_message_if_name_and_taxon_ok(self):
        self.page.create_new_individual("Kuikka", "Seppo")
        self.assertEquals("Lintu luotu onnistuneesti!", self.page.get_message().strip())

    def test_correct_message_after_save_button(self):
        self.page.create_new_individual("Kuikka", "Seppo")
        self.page.delete_individual()
        self.assertEquals("Lintu poistettu onnistuneesti!", self.page.get_message().strip())

    # def test_correct_message_after_save_button(self):
    #     self.page.create_new_individual("Kuikka", "Seppo")
    #     self.page.save_individual("Seppo","","Kuikka")
    #     self.assertEquals("Tiedot tallennettu onnistuneesti!", self.page.get_message().strip())
