from django.test import TestCase
from papukaaniApp.models_LajiStore import individual
from papukaaniApp.tests.services import LajiStoreMock

class testIndividual(TestCase):

    LajiStoreAPI = LajiStoreMock

    def test_find(self):
        LajiStoreMock.testOk = False
        individual.find(individualId = "INDIVIDUALABCD")
        self.assertTrue(LajiStoreMock.testOk)
"""
	def setUp(self):
		self.individual = {
                            "individualId" : "INDIVIDUALABCD",
                            "taxon" : "test test"
                            }

	def testCreate():
		indiv = papukaaniApp.models_LajiStore.individual.create(**self.individual)
        	self.assertEquals(True, "id" in indiv)

	def testGet():
		indiv = papukaaniApp.models_LajiStore.individual.create(**self.individual)
		indivSame = papukaaniApp.models_LajiStore.individual.get(indiv.id)
		self.assertEquals(indiv.id, indivSame.id)

	def testGetAll():
		papukaaniApp.models_LajiStore.individual.create(**self.individual)
		individual2 = {
        	"individualId" : "INDIVIDUALABCD",
            "taxon" : "test test"
            }
		papukaaniApp.models_LajiStore.individual.create(individual2)
		individuals = papukaaniApp.models_LajiStore.individual.getAll()
		self.assertEquals(2, individuals.__len__())
"""

