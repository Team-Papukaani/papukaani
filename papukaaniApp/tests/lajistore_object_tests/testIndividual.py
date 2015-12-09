from django.test import TestCase
from papukaaniApp.models_LajiStore import individual


class TestIndividual(TestCase):
    def setUp(self):
        indiv = {
            "individualId": "ABCD",
            "taxon": "test test"
        }
        indiv2 = {
            "individualId": "ABCD2",
            "taxon": "test test2"
        }

        self.ind = individual.create(**indiv)
        self.ind2 = individual.create(**indiv2)

    def tearDown(self):
        self.ind.delete()
        self.ind2.delete()

    def test_find(self):
        self.assertGreater(individual.find(individualId="ABCD").__len__(), 0)  # simple test because LajiStore not ready

    def test_get_all(self):
        individuals = individual.get_all()
        self.assertGreater(individuals.__len__(), 0)

    def test_get(self):
        self.assertEquals("ABCD", individual.get(self.ind.id).individualId)

    def test_create(self):
        self.assertEquals("ABCD", self.ind.individualId)
        self.assertEquals("test test", self.ind.taxon)
