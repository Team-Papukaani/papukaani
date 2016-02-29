from django.shortcuts import get_object_or_404, render
from papukaaniApp.models_LajiStore import gathering, document, device, individual
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from papukaaniApp.services.laji_auth_service.require_auth import require_auth
from papukaaniApp.views.decorators import count_lajistore_requests

@count_lajistore_requests
@require_auth
def devices(request):
    devices = device.find()
    devices.sort(key=lambda x: x.id)
    individuals = individual.find_exclude_deleted()

    attachments_of_devices = {dev.id: dev.get_attachments() for dev in devices}

    individual_names = {indiv.id: indiv.nickname for indiv in individuals}

    context = {
        'individuals': individuals,
        'devices': devices,
        'attachments_of_devices': json.dumps(attachments_of_devices),
        'individual_names': json.dumps(individual_names)
    }

    return render(request, 'papukaaniApp/devices.html', context)


_RESPONSE_BASE = {"errors": [], "status": ""}


@count_lajistore_requests
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

    dev = device.get(device_id)

    dev.attach_to(request.POST['individualId'], request.POST['timestamp'])

    response["status"] = "attached" if dev.is_attached() else "not attached"

    return Response(response)


@count_lajistore_requests
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

    dev = device.get(device_id)

    dev.detach_from(request.POST['individualId'], request.POST['timestamp'])

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
