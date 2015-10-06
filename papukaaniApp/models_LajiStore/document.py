from papukaaniApp.services.lajistore_service import LajiStoreAPI

class Document():
    def _init_(self, id, documentId, lastModifiedAt, lastModifiedBy, createdAt, createdBy, facts, gatherings):
        self.id = id
            self.documentId = documentId
            self.lastModifiedAt = lastModifiedAt
            self.lastModifiedBy = lastModifiedBy
            self.createdAt = createdAt
            self.createdBy = createdBy
            self.facts = facts
            self.gatherings = gatherings

    def delete(self):
        LajiStoreAPI.delete_document(self.id)

    def update(self):
        LajiStoreAPI.update_document(**self.__dict__) #__dict__ puts all arguments here

def find(**kwargs):
    return _get_many(**kwargs)

def get_all():
    return _get_many()

def get(documentID):
    document = LajiStoreAPI.get_document(documentID)
    return Document(**document)

def create(documentId, lastModifiedAt, lastModifiedBy, createdAt, createdBy, facts, gatherings):

    document = LajiStoreAPI.post_document(documentId, lastModifiedAt, lastModifiedBy, createdAt, createdBy, facts, gatherings)
    return Document(**document)

def _get_many(**kwargs): 
    data = LajiStoreAPI.get_all_documents(**kwargs)
    documents = []
    for document in data: #creates a list of documents to return
        documents.append(Document(**document))
    return documents




