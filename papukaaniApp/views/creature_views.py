from django.shortcuts import get_object_or_404, render
from papukaaniApp.models import Creature, MapPoint
import json

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
    """
    JSON format ; {"latlong" : [x,y]}
    """
    creature = get_object_or_404(Creature, pk=creature_id)
    # demcreature = Creature()  # placeholder
    # demcreature.name = "Koecreature"

    points = [{"latlong": [float(mapPoint.latitude), float(mapPoint.longitude)]} for mapPoint in MapPoint.objects.filter(creature_id=creature_id)]

    context = {
        'creature_id': creature_id,
        'creature': creature,
        'points': json.dumps(points)
    }

    return render(request, 'papukaaniApp/creature.html', context)

