import requests
from django.shortcuts import render
from django.conf import settings
import json


def validate_token(token):
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
    if "user_id" in request.session:
        del request.session["user_id"]
        return True
    return False

def require_auth(fn):
    def do_if_auth(request, *args, **kwargs):
        if authenticated(request):
            return fn(request, *args, **kwargs)
        else:
            return render(request, "papukaaniApp/login.html")

    return do_if_auth

def authenticate(request, token):
    if validate_token(token):
        log_in(request, json.loads(token)["UserDetails"]["authSourceId"])
        return True

    return False

def authenticated(request):
    if settings.MOCK_AUTHENTICATION == "Skip": return True
    else :return "user_id" in request.session




