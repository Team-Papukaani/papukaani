import json
from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging
from papukaaniApp.utils.view_utils import *
from papukaaniApp.models_LajiStore import device, document, gathering, individual
from papukaaniApp.services.laji_auth_service.require_auth import require_auth
from papukaaniApp.views.decorators import count_lajistore_requests

logger = logging.getLogger(__name__)

@require_auth
@count_lajistore_requests
def choose(request):
    """
    Controller for '/choose/'
    """

    individuals = individual.find_exclude_deleted()
    individuals_data = json.dumps({i.id: i.nickname for i in individuals})
    return render(request, 'papukaaniApp/choose.html', {'individuals_data': individuals_data})


@api_view(['POST'])
@require_auth
@count_lajistore_requests
def change_individual_gatherings(request, individual_id):
    gatherings = json.loads(request.POST['points'])
    indiv = individual.get(individual_id)
    indiv.change_gatherings(gatherings)
    return Response({'success': True})

