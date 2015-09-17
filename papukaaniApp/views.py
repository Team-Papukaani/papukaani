from django.shortcuts import render, redirect
from django.core.serializers import serialize
from .models import MapPoint
from datetime import datetime
from .utils.parser import ecotones_parse
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Creature
import timeit


def index(request):
    return render(request, 'papukaaniApp/index.html')


def public(request):
    return render(request, 'papukaaniApp/public.html')


def upload(request):
    if request.method == 'GET':
        message = request.GET['m'] if 'm' in request.GET else ''
        return render(request, 'upload.html', {"message": message})
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            try:
                data = ecotones_parse(file)
            except:
                return _redirect_with_param(upload, "?m=Tiedostosi formaatti ei ole kelvollinen!")
            points = [MapPoint(**point) for point in data]
            MapPoint.objects.bulk_create(points)

            latlongs = [[mapPoint.latitude, mapPoint.longitude] for mapPoint in points]
            return render(request, 'choose.html', {'points': latlongs})

        return _redirect_with_param(upload, "?m=Et valinnut ladattavaa tiedostoa!")


def _redirect_with_param(to, param):
    response = redirect(to)
    response['Location'] += param
    return response


def creatures(request):
    demcreature = Creature()  # placeholder
    demcreature.name = "Koecreature"
    demcreature.id = 1
    demcreature2 = Creature()  # placeholder
    demcreature2.name = "Koecreature2"
    demcreature2.id = 2

    context = {
        'creature_list': [demcreature, demcreature2]
    }

    return render(request, 'papukaaniApp/creatures.html', context)


def creature(request, creature_id):
    # creature = get_object_or_404(Creature, pk=creature_id)
    demcreature = Creature()  # placeholder
    demcreature.name = "Koecreature"
    context = {
        'creature_id': creature_id,
        'creature': demcreature
    }

    return render(request, 'papukaaniApp/creature.html', context)
