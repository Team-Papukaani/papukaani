import random
from  papukaaniApp.services.laji_auth_service.require_auth import require_auth
from django.shortcuts import render

from papukaaniApp.models_LajiStore import individual
from papukaaniApp.models_TipuApi import species

@require_auth
def individuals(request):
    """
    Controller for '/individuals/'. GET renders view,
    POST saves created or modified individual to the database
    """
    if request.method == 'POST':
        if 'id' in request.POST and 'modify' in request.POST:
            individuale = individual.get(request.POST.get('id'))
            individuale.taxon = request.POST.get('taxon')
            individuale.facts = [
                {'name': 'ring_id', 'value': request.POST.get('ring_id')},
                {'name': 'nickname', 'value': request.POST.get('nickname')},
                {'name': 'species', 'value': request.POST.get('species')},
            ]
            individuale.update()
        elif 'id' in request.POST and 'delete' in request.POST:
            individuale = individual.get(request.POST.get('id'))
            individuale.deleted = True
            individuale.update()
        elif 'taxon' in request.POST:
            individuale = individual.create(random.randint(10000000, 99999999), request.POST.get('taxon'))
            individuale.individualId = individuale.id
            individuale.update()
            # Success message

    individual_list = individual.get_all_exclude_deleted()

    populate_facts(individual_list)

    species_list = species.get_all_in_finnish()

    context = {
        'individuals': individual_list,
        'species': species_list
    }

    return render(request, 'papukaaniApp/individuals.html', context)


def populate_facts(individual_list):
    """
    Converts LajiStore facts into individual's attributes for use in the template
    """
    for individualc in individual_list:
        if individualc.facts is None:
            continue
        for fact in individualc.facts:
            setattr(individualc, fact['name'], fact['value'])