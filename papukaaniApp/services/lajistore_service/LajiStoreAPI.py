import requests
import json
from requests.auth import HTTPBasicAuth
from papukaani import secret_settings, settings

_URL = settings.LAJISTORE_URL
_AUTH = (secret_settings.LAJISTORE_USER, secret_settings.LAJISTORE_PASSWORD)
_JSON_HEADERS = {'Content-Type': 'application/json'}

#Service for LajiStore. All methods return a dictionary representing a json object, except delete methods that return a Response object.

#Devices lajistore/devices.

def get_all_devices(**kwargs):
    return _get("device")["_embedded"]["device"]

def get_device(id):
    return  _get("device/"+str(id))

def delete_device(id):
    return _delete("device/"+str(id))

def post_device(deviceId, deviceType, deviceManufacturer, createdAt, createdBy, lastModifiedAt, lastModifiedBy, facts=[]):
    data = {"deviceId":deviceId, "deviceType":deviceType, "deviceManufacturer":deviceManufacturer, "createdAt":createdAt, "createdBy":createdBy,
            "lastModifiedAt":lastModifiedAt, "lastModifiedBy": lastModifiedBy, "facts":facts}

    return _post(data, "device")

def update_device(id ,deviceId, deviceType, deviceManufacturer, createdAt, createdBy, lastModifiedAt, lastModifiedBy, facts=[]):
    data = {"id":id, "deviceId":deviceId, "deviceType":deviceType, "deviceManufacturer":deviceManufacturer, "createdAt":createdAt,
            "createdBy":createdBy, "lastModifiedAt":lastModifiedAt, "lastModifiedBy": lastModifiedBy, "facts":facts}

    return _put("device/" + str(id), data)


#Documents lajistore/documents/

def get_all_documents():
    return _get("document")["_embedded"]["document"]

def get_document(id):
    return _get("document/"+str(id))

def delete_document(id):
    return _delete("document/"+str(id))

def post_document(documentId, lastModifiedAt, lastModifiedBy, createdAt, createdBy, facts=[], gatherings=[]):
    data={"documentId":documentId, "lastModifiedAt":lastModifiedAt, "lastModifiedBy":lastModifiedBy, "createdAt":createdAt, "createdBy":createdBy, "facts":facts, "gatherings":gatherings}
    return _post(data, "document")

def update_document(id, documentId, lastModifiedAt, lastModifiedBy, createdAt, createdBy, facts=[], gatherings=[]):
    data =  {"id": id, "documentId": documentId, "lastModifiedAt": lastModifiedAt, "lastModifiedBy": lastModifiedBy,
            "createdAt": createdAt, "createdBy": createdBy, "facts": facts, "gatherings": gatherings}

    return _put("document/" + str(id), data)

#Individuals lajistore/individual

def get_all_individuals():
    return _get("individual")["_embedded"]["individual"]

def get_individual(id):
    return _get("individual/"+str(id))

def delete_individual(id):
    return _delete("individual/"+str(id))

def post_individual(individualId, taxon):
    data = {"individualId":individualId, "taxon":taxon}
    return _post(data, "individual")

def update_individual(id, individualId, taxon):
    data = {"id":id, "individualId":individualId, "taxon":taxon}
    return _put("individual/"+str(id), data)

#Private helpers:

def _delete(uri):
    url = _URL + uri
    response = requests.delete(url, auth=_AUTH)
    return response

def _get(uri, **kwargs):
    url = _URL + uri
    response = requests.get(url, auth=_AUTH).json()
    return response


def _post(data, uri):
    response = requests.post(_URL+uri, json.dumps(data), headers=_JSON_HEADERS, auth=_AUTH).json()
    return response

def _put(uri, data):
    url = _URL + uri
    response = requests.put(url, json.dumps(data), headers=_JSON_HEADERS, auth=_AUTH).json()
    return response






