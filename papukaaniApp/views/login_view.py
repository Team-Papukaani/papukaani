from django.shortcuts import redirect, render
from . import index
from papukaaniApp.services.laji_auth import authenticate, authenticated, log_in, log_out
from django.conf import settings

def login(request):
    if request.method == 'POST':
        if not "token" in request.POST:
            return redirect(login)

        if authenticate(request, request.POST["token"]):
            redirect(index)
        else: redirect(login)

    elif not authenticated(request):
        luomus_uri = "auth-sources/LTKM?target="+settings.LAJIAUTH_USER +"&next="
        haka_uri = "auth-sources/shibboleth/HAKA?target="+settings.LAJIAUTH_USER +"&next="

        if settings.MOCK_AUTHENTICATION == "On":
            log_in(request, "mock_id")
            return redirect(index)

        return render(request, "papukaaniApp/login.html", context={"haka":haka_uri, "luomus":luomus_uri, "lajiauth":settings.LAJIAUTH_URL})

    else:
        return redirect(index)

def logout(request):
    if authenticated(request):
        log_out(request)
        return redirect(index)
    return redirect(login)
