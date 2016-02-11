from django.shortcuts import get_object_or_404, render
from papukaaniApp.models_LajiStore import gathering, document, device, individual
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from papukaaniApp.services.laji_auth_service.require_auth import require_auth


@require_auth
def devices(request):
    devices = device.find()
    devices.sort(key=lambda x: x.id)
    individuals = individual.find_exclude_deleted()
    selection = individuals

    # Directory, where key is deviceId and value is an array of individual data
    individuals_of_devices = {dev.id: dev.get_individuals_for_device() for dev in devices}

    # Directory, where key is individualId and value is it's name (taxon)
    individual_names = {indiv.id: indiv.nickname if indiv.nickname != "" else indiv.id for indiv in individuals}

    context = {
        'individuals': individuals,
        'selection': selection,
        'devices': devices,
        'device_json': json.dumps(individuals_of_devices),
        'individual_json': json.dumps(individual_names)
    }

    return render(request, 'papukaaniApp/devices.html', context)


_RESPONSE_BASE = {"errors": [], "status": ""}


@api_view(['POST'])
@require_auth
def attach_to(request, device_id):
    '''
    Attach a device to an individual. Response field "status" is "attached" if attach was successful, "not attached" otherwise.
    '''
    response = _RESPONSE_BASE.copy()

    missing = _check_missing_params(request.POST, 'individualId', 'timestamp')
    if _append_missing_to_erros(response, missing):
        return Response(response)

    dev = device.find(deviceId=device_id)[0]
    indiv = individual.find(individualId=request.POST['individualId'])[0]

    attached = dev.attach_to(indiv, request.POST['timestamp'])

    response["status"] = "attached" if dev.is_attached() else "not attached"

    return Response(response)


@api_view(['POST'])
@require_auth
def remove_from(request, device_id):
    '''
    Remove a device from an individual.
    '''
    response = _RESPONSE_BASE.copy()

    missing = _check_missing_params(request.POST, 'individualId', 'timestamp')
    if _append_missing_to_erros(response, missing):
        return Response(response)

    dev = device.find(deviceId=device_id)[0]
    indiv = individual.find(individualId=request.POST['individualId'])[0]

    dev.detach_from(indiv, request.POST['timestamp'])

    return Response(response)


def _check_missing_params(collection, *args):
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
