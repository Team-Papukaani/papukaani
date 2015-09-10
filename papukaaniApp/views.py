from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def public(request):
    return render(request, 'public.html')