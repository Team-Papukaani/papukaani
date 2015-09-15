from django.shortcuts import render, redirect
from django.core.serializers import serialize
from .models import MapPoint
from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Creature


def index(request):
    return render(request, 'papukaaniApp/index.html')

def public(request):
    return render(request, 'papukaaniApp/public.html')

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

def creatures(request):

    demcreature = Creature() # placeholder
    demcreature.name = "Koecreature"
    demcreature.id = 1
    demcreature2 = Creature() # placeholder
    demcreature2.name = "Koecreature2"
    demcreature2.id = 2

    context = {
        'creature_list': [demcreature, demcreature2]
    }

    return render(request, 'papukaaniApp/creatures.html', context)

def creature(request, creature_id):

    # creature = get_object_or_404(Creature, pk=creature_id)
    demcreature = Creature() # placeholder
    demcreature.name = "Koecreature"
    context = {
        'creature_id': creature_id,
        'creature': demcreature
    }

    return render(request, 'papukaaniApp/creature.html', context)