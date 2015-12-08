from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from .views import index
from papukaaniApp.services.laji_auth_service.laji_auth import *


@csrf_exempt
def login(request):
    if request.method == 'POST':
        return _process_lajiauth_response(request)

    elif not authenticated(request):
        return _process_unauthenticated_get(request)

    else:
        return redirect(index)


def _process_unauthenticated_get(request):
    luomus_uri = "auth-sources/LTKM?target=" + settings.LAJIAUTH_USER + "&next="
    haka_uri = "auth-sources/shibboleth/HAKA?target=" + settings.LAJIAUTH_USER + "&next="
    if settings.MOCK_AUTHENTICATION == "On":
        log_in(request, "mock_id")
        return redirect(index)
    return render(request, "papukaaniApp/login.html",
                  context={"haka": haka_uri, "luomus": luomus_uri, "lajiauth": settings.LAJIAUTH_URL})


def _process_lajiauth_response(request):
    if not "token" in request.POST:
        return redirect(login)
    if authenticate(request, request.POST["token"]):
        return redirect(index)
    else:
        messages.add_message(request, messages.ERROR, "Autentikaatio ei onnistunut!")
        return redirect(login)


def logout(request):
    if authenticated(request):
        log_out(request)
        return redirect(index)
    return redirect(login)
