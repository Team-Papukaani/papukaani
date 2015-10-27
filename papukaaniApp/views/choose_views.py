import datetime
from papukaaniApp.utils.view_utils import *
from papukaaniApp.models import MapPoint
from django.shortcuts import render, redirect
from django.db.transaction import atomic
from papukaaniApp.models_LajiStore import device, document
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json


def choose(request):
    """
    Controller for '/choose/'. GET renders view,
    POST receives point publicity data as JSON and saves changes to database.

    JSON format ; {"latlong" : [x,y], "id" : int}
    """
    if request.method == 'POST':
        if 'data' in request.POST:
            _set_points_public(request)
            return redirect_with_param(choose, '?m=Valitut pisteet asetettu julkisiksi!')

        return redirect(choose)

    else:
        devices = []
        for item in device.get_all():
            devices.append(item.deviceId)
        return render(request, 'choose.html', {'devices': json.dumps(devices)})


@api_view(['GET'])
def getDocumentsForDevice(request):
    docs = document.find(deviceId=request.GET.get('devId'))
    print(docs)
    docs.
    return Response(json.dumps(docs))


def _set_points_public(request):
    docs = json.loads(request.POST['data'])
    for dict in docs:
        document.update_from_dict(**dict)
