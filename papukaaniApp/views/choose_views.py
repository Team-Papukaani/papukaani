import json
from django.shortcuts import render
from django.utils import timezone
from rest_framework.decorators import api_view
from rest_framework.response import Response
from papukaaniApp.utils.view_utils import *
from papukaaniApp.models_LajiStore import device, document, gathering, individual
from papukaaniApp.services.laji_auth_service.require_auth import require_auth
from papukaaniApp.views.decorators import count_lajistore_requests
from papukaaniApp.utils.compression import compressedBase64ToString

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
def set_individual_gatherings(request):
    gatherings = json.loads(compressedBase64ToString(request.POST['points']))
    indiv_id = request.GET['individual_id']
    indiv = individual.get(indiv_id)
    indiv.set_gatherings(gatherings)
    return Response({'success': True})

