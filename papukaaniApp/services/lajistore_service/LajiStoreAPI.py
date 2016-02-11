import requests
import json
from papukaani import secret_settings
from django.conf import settings

_URL = settings.LAJISTORE_URL
_AUTH = (secret_settings.LAJISTORE_USER, secret_settings.LAJISTORE_PASSWORD)
_JSON_HEADERS = {'Content-Type': 'application/json'}

# LajiStore resource paths:
_DEVICE_PATH = "devices"
_DOCUMENT_PATH = "documents"
_INDIVIDUAL_PATH = "individuals"
_DEVICEINDIVIDUAL_PATH = "deviceIndividual"

_ERROR_MSG = "Error while saving to LajiStore. Check arguments!"


# Service for LajiStore. All methods return a dictionary representing a json object, except delete methods that return a Response object. Query arguments can be passed to get_all_* methods
# as keyword parameters. For example get_all_devices(deviceType="exampleType") returns all devices with deviceType "exampleType".


# DeviceIndividuals lajistore/deviceIndividual/

def get_all_deviceindividual(**kwargs):
    return _get_all_pages(_DEVICEINDIVIDUAL_PATH, **kwargs)


def get_deviceindividual(id):
    return _get(_DEVICEINDIVIDUAL_PATH + "/" + str(id))


def delete_deviceindividual(id):
    return _delete(_DEVICEINDIVIDUAL_PATH + "/" + str(id))


def post_deviceindividual(**data):
    return _post(data, _DEVICEINDIVIDUAL_PATH)


def update_deviceindividual(**data):
    return _put(_DEVICEINDIVIDUAL_PATH + "/" + str(data["id"]), data)


def delete_all_deviceindividual():
    return _delete(_DEVICEINDIVIDUAL_PATH)


# Devices lajistore/devices.

def get_all_devices(**kwargs):
    return _get_all_pages(_DEVICE_PATH, **kwargs)


def get_device(id):
    return _get(_DEVICE_PATH + "/" + str(id))


def delete_device(id):
    return _delete(_DEVICE_PATH + "/" + str(id))


def post_device(**data):
    return _post(data, _DEVICE_PATH)


def update_device(**data):
    id = str(data["id"])
    return _put(_DEVICE_PATH + "/" + id, data)


def delete_all_devices():
    return _delete(_DEVICE_PATH)


# Documents lajistore/documents/

def get_all_documents(**kwargs):
    return _get_all_pages(_DOCUMENT_PATH, **kwargs)


def get_document(id):
    return _get(_DOCUMENT_PATH + "/" + str(id))


def delete_document(id):
    return _delete(_DOCUMENT_PATH + "/" + str(id))


def post_document(**data):
    return _post(data, _DOCUMENT_PATH)


def update_document(**data):
    return _put(_DOCUMENT_PATH + "/" + str(data["id"]), data)


def delete_all_documents():
    return _delete(_DOCUMENT_PATH)


# Individuals lajistore/individual

def get_all_individuals(**kwargs):
    return _get_all_pages(_INDIVIDUAL_PATH, **kwargs)


def get_individual(id):
    return _get(_INDIVIDUAL_PATH + "/" + str(id))


def delete_individual(id):
    return _delete(_INDIVIDUAL_PATH + "/" + str(id))


def post_individual(**data):
    return _post(data, _INDIVIDUAL_PATH)


def update_individual(**data):
    return _put(_INDIVIDUAL_PATH + "/" + str(data["id"]), data)


def delete_all_individuals():
    return _delete(_INDIVIDUAL_PATH)


# Private helpers:

def _delete(uri):
    url = _URL + uri
    response = requests.delete(url, auth=_AUTH)
    if '@id' in response:
        response['id'] = response['@id'].rsplit('/', 1)[-1]
    return response


def _get(uri, **kwargs):
    url = _URL + uri
    if kwargs:
        url += _add_query(**kwargs)
    response = requests.get(url, auth=_AUTH).json()
    if '@id' in response:
        response['id'] = response['@id'].rsplit('/', 1)[-1]
    return response


def _post(data, uri):
    return _create_response(data, uri, True)


def _put(uri, data):
    return _create_response(data, uri, False)


def _create_response(data, uri, post):
    url = _URL + uri
    if 'id' in data: del data['id']
    if '@id' in data: del data['@id']

    if (post):
        response = requests.post(url, json.dumps(data), headers=_JSON_HEADERS, auth=_AUTH).json()
    else:
        response = requests.put(url, json.dumps(data), headers=_JSON_HEADERS, auth=_AUTH).json()

    if "@id" not in response:
        raise ValueError(_ERROR_MSG)

    response['id'] = response['@id'].rsplit('/', 1)[-1]
    return response


def _add_query(**kwargs):
    q = ""
    if 'filter' in kwargs:
        q += "?filter="
        q = _parse_query_param(kwargs["filter"], q)
        kwargs.pop("filter")

    if len(kwargs.keys()) > 0:
        q += "?q=" if q == "" else "&q="
        q = _parse_query_param(kwargs, q)

    return q


def _parse_query_param(kwargs, q):
    initial = q
    for k in kwargs:
        k_name = k.replace("_", ".")
        q += "" if q == initial else " AND "
        q += k_name + ":" + str(kwargs[k])
    return q


def _get_all_pages(url, list=None, **kwargs):
    response = _get(url, **kwargs)

    if response['totalItems'] == 0:
        return []

    members = response['member']

    for member in members:
        if '@id' in member:
            member['id'] = member['@id'].rsplit('/', 1)[-1]

    list = list + members if list else members

    if response['view']['@id'] == response['view']['lastPage']:
        return list

    else:
        url = response['view']['nextPage'].rsplit('/', 1)[-1]
        return _get_all_pages(url, list)
