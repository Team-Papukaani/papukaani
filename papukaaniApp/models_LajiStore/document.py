from papukaaniApp.services.lajistore_service import LajiStoreAPI

class Document():
	def _init_(self, documentID, lastModifiedAt, lastModifiedBy, createdAt, createdBy, facts, gatherings):
    		self.documentID = documentID
    		self.lastModifiedAt = lastModifiedAt
    		self.lastModifiedBy = lastModifiedBy
    		self.createdAt = createdAt
    		self.createdBy = createdBy
    		self.facts = facts
    		self.gatherings = gatherings

def all():
	data = LajiStoreAPI.get_all_documents():
	documents = []
	for document in data:
		documentss.append(Document(**document))
	return documents

