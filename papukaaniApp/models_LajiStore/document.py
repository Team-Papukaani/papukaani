from papukaaniApp.services.lajistore_service import LajiStoreAPI
from papukaaniApp.models_LajiStore import gathering

class Document():
    '''
    Represents the LajiStore table Document
    '''
    def __init__(self, id, documentId, lastModifiedAt, lastModifiedBy, createdAt, createdBy, facts, gatherings, **kwargs):
        self.id = id
        self.documentId = documentId
        self.lastModifiedAt = lastModifiedAt
        self.lastModifiedBy = lastModifiedBy
        self.createdAt = createdAt
        self.createdBy = createdBy
        self.facts = facts
        self.gatherings = _parse_gathering(gatherings)

    def delete(self):
        '''
        Deletes the document from LajiStore. Note that the object is not destroyed!
        '''
        LajiStoreAPI.delete_document(self.id)

    def update(self):
        '''
        Saves changes to the object to the corresponding LajiStore entry.
        '''
        dict = self.__dict__
        dict["gatherings"] = [g.to_lajistore_json() for g in self.gatherings]
        LajiStoreAPI.update_document(**dict) #__dict__ puts all arguments here

def find(**kwargs):
    '''
    Find all matching documents.
    :param kwargs: Search parameters.
    :return: A list of Document objects.
    '''
    return _get_many(**kwargs)


def get_all():
    '''
    Returns all documents
    :return A list of Document objects:
    '''
    return _get_many()

def get(id):
    '''
    Gets a document from LajiStore
    :param id: The LajiStore ID of the document
    :return: A Document object
    '''
    document = LajiStoreAPI.get_document(id)
    return Document(**document)


def create(documentId, lastModifiedAt, lastModifiedBy, createdAt, createdBy, facts, gatherings):
    '''
    Creates a document instance in LajiStore and a corresponding Document object
    :return: A Document object
    '''
    document = LajiStoreAPI.post_document(documentId, lastModifiedAt, lastModifiedBy, createdAt, createdBy, facts, gatherings)
    return Document(**document)


def _get_many(**kwargs):
    data = LajiStoreAPI.get_all_documents(**kwargs)
    documents = []
    for document in data:  # creates a list of documents to return
        documents.append(Document(**document))
    return documents


def _parse_gathering(data):
    return  [gathering.from_lajistore_json(**point) for point in data]


