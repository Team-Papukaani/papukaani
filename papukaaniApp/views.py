from django.shortcuts import render, redirect
from django.core.serializers import serialize
from .models import MapPoint
from datetime import datetime
from .utils.parser import ecotones_parse


def index(request):
    return render(request, 'index.html')

def public(request):
    return render(request, 'public.html')


def upload(request):
    if request.method == 'GET':
        message = request.GET['m'] if 'm' in request.GET else ''
        return render(request, 'upload.html', {"message" : message})
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            try:
                data = ecotones_parse(file)
            except:
                return _redirect_with_param(upload, "?m=Tiedostosi formaatti ei ole kelvollinen!")
            points = [MapPoint.objects.create(**point) for point in data]
            return render(request, 'upload.html', {'points': serialize('json', points)})

        return _redirect_with_param(upload, "?m=Et valinnut ladattavaa tiedostoa!")

def _redirect_with_param(to, param):
    response = redirect(to)
    response['Location'] += param
    return response