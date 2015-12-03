import json

from django.shortcuts import render, get_object_or_404

from papukaaniApp.models import *
from papukaaniApp.models_TipuApi import species
from papukaaniApp.utils.view_utils import extract_latlongs
from django.views.decorators.clickjacking import xframe_options_exempt
from papukaaniApp.models_LajiStore import *


@xframe_options_exempt  # Allows the view to be loaded in an iFrame
def public(request):
    """
    Controller for '/public/'.
    """

    individuals = dict()
    for individuale in individual.get_all_exclude_deleted():
        key = individuale.get_facts_as_dictionary()['species']
        individuals.setdefault(key, [])
        individuals[key].append({individuale.individualId: individuale.taxon})

    all_species = species.get_all_in_finnish()
    ordered_species = []
    for s in all_species:
        if s.id in individuals:
            individuals[s.name] = individuals.pop(s.id)  # Renames the species id to Finnish
            ordered_species.append(s.name)
    ordered_species.sort()

    context = { 'individuals': json.dumps(individuals),
                'species': json.dumps(ordered_species)
               }

    return render(request, 'papukaaniApp/public.html', context)
