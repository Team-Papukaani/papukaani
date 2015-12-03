from papukaaniApp.services.laji_auth_service.laji_auth import authenticated

def auth(request):
    return {"authenticated" : authenticated(request)}