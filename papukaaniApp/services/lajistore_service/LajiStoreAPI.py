import requests
import json
from papukaani import secret_settings, settings

_URL = settings.LAJISTORE_URL
_AUTH = (secret_settings.LAJISTORE_USER, secret_settings.LAJISTORE_PASSWORD)
_JSON_HEADERS = {'Content-Type': 'application/json'}

#Service for LajiStore. All methods return a dictionary representing a json object, except delete methods that return a Response object. Query arguments can be passed to get_all_* methods
#as keyword parameters. For example get_all_devices(deviceType="exampleType") returns all devices with deviceType "exampleType".

#Devices lajistore/devices.

def get_all_devices(**kwargs):
    return _get_all_pages("device","device",**kwargs)

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

def get_all_documents(**kwargs):
    return _get_all_pages("document", "document",**kwargs)

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

def get_all_individuals(**kwargs):
    return _get_all_pages("individual","individual", **kwargs)

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
    if(kwargs):
        url += _add_query(**kwargs)
    response = requests.get(url, auth=_AUTH).json()
    return response


def _post(data, uri):
    response = requests.post(_URL+uri, json.dumps(data), headers=_JSON_HEADERS, auth=_AUTH).json()
    return response

def _put(uri, data):
    url = _URL + uri
    response = requests.put(url, json.dumps(data), headers=_JSON_HEADERS, auth=_AUTH).json()
    return response

def _add_query(**kwargs):
    q = "?query="
    for k in kwargs:
        q += "" if q == "?query=" else " AND "
        q += k +":"+str(kwargs[k])

    return q

def _get_all_pages(uri, key, list = None, **kwargs):

    response = _get(uri, **kwargs)
    embedded = response["_embedded"][key]
    list = list + embedded if list else embedded
    links = response["_links"]

    if links["self"]["href"] == links["last"]["href"]:
        return list

    else:
        uri = links["next"]["href"].split("/")[-1]
        return _get_all_pages(uri, key, list)





