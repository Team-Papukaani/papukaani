from django.conf import settings
import requests
from papukaani import secret_settings

_URL = settings.TIPUAPI_URL
_AUTH = (secret_settings.TIPUAPI_USER, secret_settings.TIPUAPI_PASSWORD)

# Service for TipuApi. The method returns a dictionary representing a json object

def get_all_species():
    url = _URL + "?format=json"
    response = requests.get(url, auth=_AUTH).json()

    return response


