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

    devices = []
    for item in device.get_all():
        devices.append(item.deviceId)
    devices.sort()

    individuals = dict()
    for individuale in individual.get_all_exclude_deleted():
        key = individuale.get_facts_as_dictionary()['species']
        individuals.setdefault(key, [])
        individuals[key].append({individuale.individualId: individuale.taxon})
    #
    # print(json.dumps(individuals))

    # individuals = []
    # for individuale in individual.get_all_exclude_deleted():
    #     individuals.append({individuale.individualId: individuale.taxon})

    context = {'devices': json.dumps(devices),
               'individuals': json.dumps(individuals)
               }

    return render(request, 'papukaaniApp/public.html', context)
