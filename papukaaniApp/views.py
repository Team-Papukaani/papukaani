from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import RequestContext, loader
from .models import Creature

def index(request):
    return render(request, 'papukaaniApp/index.html')

def public(request):
    return render(request, 'papukaaniApp/public.html')

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