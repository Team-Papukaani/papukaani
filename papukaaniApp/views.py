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
        file = request.FILES['file']
        data = ecotones_parse(file)
        points = [MapPoint.objects.create(**point) for point in data]
        return render(request, 'index.html', {'points': serialize('json', points)})
    return redirect(index)


def ecotones_parse(file):
    entries = []
    with file as f:
        lines = [line for line in f]
    for i in range(1, len(lines)):
        fields = str(lines[i]).split(',')
        alt = fields[15]
        if len(alt) == 0:
            alt = 0
        e_dict = {"timestamp": parsetime(fields[2]), "latitude": float(fields[4]), "longitude": float(fields[5]),
                  "altitude": float(alt),
                  "temperature": float(fields[8])};
        entries.append(e_dict)
    return entries


def parsetime(timestring):
    return datetime.strptime(timestring, "%Y-%m-%d %H:%M:%S")
