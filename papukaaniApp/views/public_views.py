import json

from django.shortcuts import render, get_object_or_404

from papukaaniApp.models import *
from papukaaniApp.utils.view_utils import extract_latlongs
from django.views.decorators.clickjacking import xframe_options_exempt
from papukaaniApp.models_LajiStore import *

@xframe_options_exempt  #Allows the view to be loaded in an iFrame
def public(request, creature_id):
    """
    Controller for '/public/'.
    """

    docs = document.find(deviceId=creature_id, gatherings_publicity="public")
    points = []
    for doc in docs:
        points += doc.gatherings

    latlongs = [point.geometry for point in points]

    return render(request, 'papukaaniApp/public.html', {"points": json.dumps(latlongs)})



