import requests
from django.shortcuts import redirect
from django.conf import settings
import json

def validate_token(token):
    token = token.encode("utf-8")
    url = settings.LAJIAUTH_URL + "validation/"
    print(token)
    response = requests.post(url, data=token, headers={"Content-Type":"application/json"})

    print(response.status_code)
    print(response.content)

    if response.status_code == 200:
        return True
    else: return False

def log_in(request, id):
    if not "user_id" in request.session:
        request.session["user_id"] = id
        return True
    return False

def log_out(request):
    if "user_id" in request.session:
        del request.session["user_id"]
        return True
    return False

def authenticate(request, token):
    if validate_token(token):
        log_in(request, json.loads(token)["user"]["authSourceId"])
        return True

    return False

def authenticated(request):
    if settings.MOCK_AUTHENTICATION == "Skip": return True
    else :return "user_id" in request.session




