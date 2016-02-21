import random
from  papukaaniApp.services.laji_auth_service.require_auth import require_auth
from django.shortcuts import render

from papukaaniApp.models_LajiStore import individual
from papukaaniApp.models_TipuApi import species

from django.contrib import messages

from django.utils.translation import ugettext_lazy as _


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
    individuale.ringID = request.POST.get('ring_id')
    individuale.nickname = request.POST.get('nickname')
    descriptionFields = _getDescriptionFields(request)
    individuale.description = descriptionFields[0]
    individuale.descriptionURL = descriptionFields[1]
    individuale.update()
    messages.add_message(request, messages.INFO, _('Tiedot tallennettu onnistuneesti!'))


def _delete_individual(request):
    individuale = individual.get(request.POST.get('id'))
    individuale.deleted = True
    individuale.update()
    messages.add_message(request, messages.INFO, _('Lintu poistettu onnistuneesti!'))


def _create_individual(request):
    if not _post_is_valid(request):
        return _return_with_context(request)

    descriptionFields = _getDescriptionFields(request)
    individual.create(request.POST.get('nickname'), request.POST.get('taxon'),
                      description=descriptionFields[0] or None, descriptionURL=descriptionFields[1] or None)
    messages.add_message(request, messages.INFO, _('Lintu luotu onnistuneesti!'))


def _getDescriptionFields(request):
    descriptionFields = [{}, {}]
    descriptionFields[0]['en'] = request.POST.get('descriptionEN')
    descriptionFields[0]['fi'] = request.POST.get('descriptionFI')
    descriptionFields[0]['sv'] = request.POST.get('descriptionSV')
    descriptionFields[1]['en'] = request.POST.get('descriptionUrlEN')
    descriptionFields[1]['fi'] = request.POST.get('descriptionUrlFI')
    descriptionFields[1]['sv'] = request.POST.get('descriptionUrlSV')
    return descriptionFields


def _post_is_valid(request):
    if request.POST.get('taxon') == "":
        messages.add_message(request, messages.ERROR, _('Laji puuttuu!'))
        return False

    if request.POST.get('nickname') == "":
        messages.add_message(request, messages.ERROR, _('Nimi puuttuu!'))
        return False

    return True


def _return_with_context(request):
    individual_list = individual.find_exclude_deleted()
    try:
        species_list = species.get_all_in_user_language(request.LANGUAGE_CODE)
    except:
        species_list = []

    context = {
        'individuals': individual_list,
        'species': species_list
    }
    return render(request, 'papukaaniApp/individuals.html', context)
