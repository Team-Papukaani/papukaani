from django.test import TestCase
from papukaaniApp.models_LajiStore import individual

class testIndividual(TestCase):

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

)
