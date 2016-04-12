from papukaaniApp.services.lajistore_service import LajiStoreAPI
from papukaaniApp.models_LajiStore import gathering
from papukaaniApp.utils.model_utils import *
from django.conf import settings

_LAJISTORE_COLLECTIONID = settings.LAJISTORE_COLLECTIONID


class Document:
    '''
    Represents the LajiStore table Document
    '''

    def __init__(self, gatherings, deviceID, dateCreated, dateEdited, collectionID=None, id=None):

        if len(gatherings) > 0 and isinstance(gatherings[0], gathering.Gathering):
            self.gatherings = gatherings
        else:
            self.gatherings = _parse_gathering(gatherings)

        self.collectionID = collectionID if collectionID else _LAJISTORE_COLLECTIONID
        self.deviceID = deviceID
        self.dateCreated = dateCreated
        self.dateEdited = dateEdited
        self.id = id

    def delete(self):
        '''
        Deletes the document from LajiStore. Note that the object is not destroyed!
        '''
        LajiStoreAPI.delete_document(self.id)

    def update(self):
        '''
        Saves changes to the object to the corresponding LajiStore entry.
        '''

        self.dateEdited = current_time_as_lajistore_timestamp()
        dict = self.to_dict()
        LajiStoreAPI.update_document(**dict)  # to_dict() puts all arguments here

    def to_dict(self):
        dict = self.__dict__.copy()
        dict["gatherings"] = [g.to_lajistore_json() for g in self.gatherings]
        return dict


def find(**kwargs):
    '''
    Find all matching documents.
    :param kwargs: Search parameters.
    :return: A list of Document objects.
    '''
    data = LajiStoreAPI.get_all_documents(**kwargs)
    documents = []
    for document in data:  # creates a list of documents to return
        documents.append(Document(**document))
    return documents


def get(id):
    '''
    Gets a document from LajiStore
    :param id: The LajiStore ID of the document
    :return: A Document object
    '''
    document = LajiStoreAPI.get_document(id)
    return Document(**document)


def create(gatherings, deviceID, dateCreated=None, dateEdited=None):
    '''
    Creates a document instance in LajiStore and a corresponding Document object
    :return: A Document object
    '''
    current_time = current_time_as_lajistore_timestamp()
    dateCreated = dateCreated if dateCreated else current_time
    dateEdited = dateEdited if dateEdited else current_time
    document = Document(gatherings, deviceID, dateCreated, dateEdited)
    data = LajiStoreAPI.post_document(**document.to_dict())
    document.id = data["id"]

    return document


def _parse_gathering(data):
    return [gathering.from_lajistore_json(**point) for point in data]


def delete_all():
    '''
    Deletes all documents. Can only be used in test enviroment.
    '''
    LajiStoreAPI.delete_all_documents()
