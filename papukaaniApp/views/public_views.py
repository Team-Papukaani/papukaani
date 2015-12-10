import json

from django.shortcuts import render, get_object_or_404

from papukaaniApp.models import *
from papukaaniApp.utils.view_utils import extract_latlongs
from django.views.decorators.clickjacking import xframe_options_exempt
from papukaaniApp.models_LajiStore import *


@xframe_options_exempt  # Allows the view to be loaded in an iFrame
def public(request):
    """
    Controller for '/public/'.
    """

    individuals = []
    for item in individual.get_all():
        individuals.append(item.individualId)
    individuals = [{individual.facts : }]

    individuals.sort()
    return render(request, 'papukaaniApp/public.html', {'devices': json.dumps(individuals)})


