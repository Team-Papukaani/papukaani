from django.shortcuts import get_object_or_404, render
from papukaaniApp.models_LajiStore import gathering, document, device, individual
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response


def devices(request):

    devices = device.get_all()
    individuals = individual.get_all()

    context = {
        'individuals': individuals,
        'devices': devices
    }

    return render(request, 'papukaaniApp/devices.html', context)


_RESPONSE_BASE = {"errors" : []}

@api_view(['POST'])
def attach_to(request, device_id):
    '''
    Attach a device to an individual.
    '''
    response = _RESPONSE_BASE.copy()

    missing = _check_missing_params(request.POST, 'individualId', 'timestamp')
    if _append_missing_to_erros(response, missing):
        return Response(response)

    dev = device.find(deviceId = device_id)[0]
    indiv = individual.find(individualId = request.POST['individualId'])[0]

    dev.attach_to(indiv, request.POST['timestamp'])
    dev.update()
    return Response(response)

@api_view(['POST'])
def remove_from(request, device_id):
    '''
    Remove a device from an individual.
    '''
    response = _RESPONSE_BASE.copy()

    missing = _check_missing_params(request.POST, 'individualId')
    if _append_missing_to_erros(response, missing):
        return Response(response)

    dev = device.find(deviceId = device_id)[0]
    indiv = individual.find(individualId = request.POST['individualId'])[0]

    dev.remove_from(indiv)
    dev.update()

    return Response(response)



def _check_missing_params(collection ,*args):
    missing = []
    for param in args:
        if not param in collection:
            missing.append(param)

    return missing

def _append_missing_to_erros(response, missing):
    if len(missing) > 0:
        response["errors"].append("Arguments missing: " + str(missing))
        return True
    return False

