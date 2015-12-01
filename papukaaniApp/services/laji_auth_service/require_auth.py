from papukaaniApp.views.login_view import *

def require_auth(fn):
    def do_if_auth(request, *args, **kwargs):
        if authenticated(request):
            return fn(request, *args, **kwargs)
        else:
            return redirect(login)

    return do_if_auth