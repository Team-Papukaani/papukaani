from django.shortcuts import redirect, render
from . import choose

def login(request):
    if request.method == 'GET':
        return render(request, "papukaaniApp/login.html")