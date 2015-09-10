from django.shortcuts import render, redirect
from django.core.serializers import serialize
from .models import MapPoint
from datetime import datetime

def index(request):
    return render(request, 'index.html')

def public(request):
    return render(request, 'public.html')

def upload(request):
    if request.method == 'POST' and 'file' in request.FILES:
        file =request.FILES['file'].read()

        data = [{"timestamp": datetime.now(), "latitude":22.222, "longitude":22.222, "altitude":234.22, "temperature":22.23},
                {"timestamp": datetime.now(), "latitude":22.022, "longitude":22.122, "altitude":234.22, "temperature":22.23},
                {"timestamp": datetime.now(), "latitude":22.122, "longitude":22.022, "altitude":234.22, "temperature":22.23}]
        ##data = parse(file)
        points = []
        for point in data:
            points.append(MapPoint.objects.create(**point))

        return render(request, 'index.html', {'points' : serialize('json', points)})

    return redirect(index)