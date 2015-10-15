import json

from django.shortcuts import render, get_object_or_404

from papukaaniApp.models import *
from papukaaniApp.utils.view_utils import extract_latlongs
from django.views.decorators.clickjacking import xframe_options_exempt

@xframe_options_exempt  #Allows the view to be loaded in an iFrame
def public(request, creature_id):
    """
    Controller for '/public/'.
    """

    creature = get_object_or_404(Creature, pk=creature_id)

    points = creature.return_public_points()

    latlongs = extract_latlongs(points)

    return render(request, 'papukaaniApp/public.html', {"points": json.dumps(latlongs)})



