from django.contrib.sites.models import get_current_site
from django.shortcuts import get_object_or_404, render
from papukaaniApp.models import Creature, MapPoint
import json
from papukaaniApp.utils.view_utils import extract_latlongs


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
    JSON format: [[61.757366, 22.344783], [61.757366, 22.344966]
    """

    creature = get_object_or_404(Creature, pk=creature_id)

    points = creature.return_public_points()

    latlongs = extract_latlongs(points)

    context = {
        'creature_id': creature_id,
        'creature': creature,
        'points': json.dumps(latlongs),
        'server_url': 'http://' + get_current_site(request).domain
    }

    return render(request, 'papukaaniApp/creature.html', context)
