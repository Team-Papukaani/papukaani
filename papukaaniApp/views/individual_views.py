import random
from  papukaaniApp.services.laji_auth_service.require_auth import require_auth
from django.shortcuts import render

from papukaaniApp.models_LajiStore import individual
from papukaaniApp.models_TipuApi import species

from django.contrib import messages

@require_auth
def individuals(request):
    """
    Controller for '/individuals/'. GET renders view,
    POST saves created or modified individual to the database
    """
    if request.method == 'POST':
        if 'id' in request.POST and 'modify' in request.POST:
            _update_individual(request)
        elif 'id' in request.POST and 'delete' in request.POST:
            _delete_individual(request)
        elif 'taxon' in request.POST:
            _create_individual(request)
    return _return_with_context(request)

def _update_individual(request):
    if not _post_is_valid(request):
        return _return_with_context(request)

    individuale = individual.get(request.POST.get('id'))
    individuale.taxon = request.POST.get('taxon')
        # {'name': 'ring_id', 'value': request.POST.get('ring_id')},
    individuale.update()
    messages.add_message(request, messages.INFO, 'Tiedot tallennettu onnistuneesti!')

def _delete_individual(request):
    individuale = individual.get(request.POST.get('id'))
    individuale.deleted = True
    individuale.update()
    messages.add_message(request, messages.INFO, 'Lintu poistettu onnistuneesti!')

def _create_individual(request):
    if not _post_is_valid(request):
        return _return_with_context(request)

    individuale = individual.create(request.POST.get('nickname'),request.POST.get('taxon'))
    messages.add_message(request, messages.INFO, 'Lintu luotu onnistuneesti!')

def _post_is_valid(request):
    if request.POST.get('taxon') == "":
        messages.add_message(request, messages.ERROR, 'Laji puuttuu!')
        return False

    if request.POST.get('nickname') == "":
        messages.add_message(request, messages.ERROR, 'Nimi puuttuu!')
        return False
    return True

def _return_with_context(request):
    individual_list = individual.find_exclude_deleted()
    try:
        species_list = species.get_all_in_finnish()
    except:
        species_list = []

    context = {
        'individuals': individual_list,
        'species': species_list
    }
    return render(request, 'papukaaniApp/individuals.html', context)
