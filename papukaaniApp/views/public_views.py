import json

from django.shortcuts import render, get_object_or_404

from papukaaniApp.models import *
from papukaaniApp.utils.view_utils import extract_latlongs
from django.views.decorators.clickjacking import xframe_options_exempt
from papukaaniApp.models_LajiStore import *
from papukaaniApp.views.login_view import *


@xframe_options_exempt  # Allows the view to be loaded in an iFrame
def public(request):
    """
    Controller for '/public/'.
    """
    individuals = [indiv.individualId for indiv in individual.get_all()]

    individuals.sort()

    display_navigation = authenticated(request)

    context = { 'devices': json.dumps(individuals),
                'display_navigation': display_navigation,
                'device': request.GET.get('device', ''),
                'speed': request.GET.get('speed', '')
    }

    return render(request, 'papukaaniApp/public.html', context)



