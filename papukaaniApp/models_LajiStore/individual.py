from papukaaniApp.services.lajistore_service import LajiStoreAPI

class Individual():
	def _init_(self, id, individualId, taxon):
		self.id = id
		self.individualId = individualId
		self.taxon = taxon
	
	def delete(self):
		LajiStoreAPI.delete_individual(self.id)

	def update(self):
		LajiStoreAPI.update_individual(**self.__dict__) #__dict__ puts all arguments here

def find(**kwargs): #tests!
	return _get_many(**kwargs)	
	

def get_all(): 
	return _get_many()
	
def get(individualId):
	individual = LajistoreAPI.get_individual(individualId)
	return Individual(**individual)

def create(individualId, taxon):	
	individual = LajiStoreAPI.post_individual(individualId, taxon)
	return Individual(**individual)

def _get_many(**kwargs): 
	data = LajiStoreAPI.get_all_individuals(**kwargs):
	individuals = []
	for individual in data: #creates a list of individuals to return
		individuals.append(Individual(**individual))
	return individuals
	

