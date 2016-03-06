import json

from django.shortcuts import render, get_object_or_404

from papukaaniApp.models import *
from papukaaniApp.models_TipuApi import species
from papukaaniApp.utils.view_utils import extract_latlongs
from django.views.decorators.clickjacking import xframe_options_exempt
from papukaaniApp.models_LajiStore import *
from papukaaniApp.views.login_view import *
from papukaaniApp.views.decorators import count_lajistore_requests


@count_lajistore_requests
@xframe_options_exempt  # Allows the view to be loaded in an iFrame
def public(request):
    """
    Controller for '/public/'.
    """
    individuals = dict()
    inds_objects = individual.find_exclude_deleted()
    for individuale in inds_objects:
        key = individuale.taxon
        individuals.setdefault(key, [])
        individualInfo = {'nickname': individuale.nickname,
                          'description': individuale.description,
                          'descriptionURL': individuale.descriptionURL
                          }

        individuals[key].append({individuale.id: individualInfo})

    all_species = species.get_all_in_user_language(request.LANGUAGE_CODE)
    ordered_species = []
    for s in all_species:
        if s.id in individuals:
            individuals[s.name] = individuals.pop(s.id)  # Renames the species
            ordered_species.append(s.name)
    ordered_species.sort()

    display_navigation = authenticated(request)

    extended = 'base.html'
    if display_navigation:
        extended = 'base_with_nav.html'

    context = {'individuals': json.dumps(individuals),
               'species': json.dumps(ordered_species),
               'display_navigation': display_navigation,
               'individualIds': request.GET.get('individuals', []),
               'speed': request.GET.get('speed', ''),
               'loc': request.GET.get('loc', [61.0, 20.0]),
               'zoom': request.GET.get('zoom', 5),
               'start_time': request.GET.get('start_time', ''),
               'end_time': request.GET.get('end_time', ''),
               'extended': extended
               }

    return render(request, 'papukaaniApp/public.html', context)
