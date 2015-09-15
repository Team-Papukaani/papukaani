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
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            data = ecotones_parse(file)
            points = [MapPoint.objects.create(**point) for point in data]
            return render(request, 'index.html', {'points': serialize('json', points)})
        return redirect(index)
    return redirect(index)

