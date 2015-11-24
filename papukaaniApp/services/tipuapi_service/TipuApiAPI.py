import requests
import json
from papukaani import secret_settings
from django.conf import settings
from time import clock

_URL = "https://fmnh-ws-test.it.helsinki.fi/tipu-api/species" #settings.LAJISTORE_URL
_AUTH = ("papukaanit", "SKL4hhdsjh4") #(secret_settings.LAJISTORE_USER, secret_settings.LAJISTORE_PASSWORD)


# Service for LajiStore. All methods return a dictionary representing a json object, except delete methods that return a Response object. Query arguments can be passed to get_all_* methods
# as keyword parameters. For example get_all_devices(deviceType="exampleType") returns all devices with deviceType "exampleType".



def get_all_species():
    url = _URL + "?format=json"
    response = requests.get(url, auth=_AUTH).json()

    return response


