import requests
from django.shortcuts import redirect
from django.conf import settings
import json

def _validate_token(token):
    token = token.encode("utf-8")
    url = settings.LAJIAUTH_URL + "validation/"

    response = requests.post(url, data=token, headers={"Content-Type":"application/json"})

    if response.status_code == 200:
        return True
    else: return False

def log_in(request, id):
    if not "user_id" in request.session:
        request.session["user_id"] = id
        return True
    return False

def log_out(request):
    '''
    Clear session for the request.
    :param request:
    :return: true if user was succesfully logged out
    '''
    if "user_id" in request.session:
        del request.session["user_id"]
        return True
    return False

def authenticate(request, token):
    '''
    Logs user in if the token is valid.
    :param request: A HttpRequest to create session for
    :param token: The token returned by LajiAuth.
    :return: true if user is authenticated succesfully
    '''
    if _validate_token(token):
        log_in(request, json.loads(token)["user"]["authSourceId"])
        return True

    return False

def authenticated(request):
    '''
    Checks if user is authenticated if MOCK_AUTHENTICATION is set to 'Skip', always returns true,
    :param request:
    :return:
    '''
    if settings.MOCK_AUTHENTICATION == "Skip": return True
    else :return "user_id" in request.session




