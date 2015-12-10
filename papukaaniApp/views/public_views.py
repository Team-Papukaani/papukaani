import json

from django.shortcuts import render, get_object_or_404

from papukaaniApp.models import *
from papukaaniApp.utils.view_utils import extract_latlongs
from django.views.decorators.clickjacking import xframe_options_exempt
from papukaaniApp.models_LajiStore import *
from papukaaniApp.views.login_view import *
from papukaaniApp.utils.view_utils import populate_facts


@xframe_options_exempt  # Allows the view to be loaded in an iFrame
def public(request):
    """
    Controller for '/public/'.
    """
    inds = individual.get_all_exclude_deleted()
    populate_facts(inds)

    individuals = [{"id" : indiv.individualId, "nickname" : indiv.nickname }for indiv in inds if hasattr(indiv, "nickname")]

    display_navigation = authenticated(request)

    context = { 'devices': json.dumps(individuals),
                'display_navigation': display_navigation,
                'device': request.GET.get('device', ''),
                'speed': request.GET.get('speed', '')
    }

    return render(request, 'papukaaniApp/public.html', context)



