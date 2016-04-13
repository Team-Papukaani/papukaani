from django.http import QueryDict, JsonResponse
from django.shortcuts import get_object_or_404, render
from papukaaniApp.models_LajiStore import gathering, document, device, individual
from papukaaniApp.services.deviceindividual_service import DeviceIndividual
from papukaaniApp.services.deviceindividual_service.DeviceIndividual import AlreadyHasDevice, DeviceAlreadyAttached
import json
from rest_framework.decorators import api_view
from rest_framework.response import Response
from papukaaniApp.services.laji_auth_service.require_auth import require_auth
from papukaaniApp.views.decorators import count_lajistore_requests
from django.utils.translation import ugettext as _
import logging
import traceback

logger = logging.getLogger(__name__)

def _responseBase():
    return {"errors": [], "status": "OK", "data": {}}

@count_lajistore_requests
@require_auth
def devices(request):
    devices = device.find()
    devices.sort(key=lambda x: x.id)
    individuals = individual.find_exclude_deleted()

    context = {
        'individuals': individuals,
        'devices': devices,
        'individuals_json': json.dumps([i.to_dict() for i in individuals]),
        'devices_json': json.dumps([d.to_dict() for d in devices]),
    }

    return render(request, 'papukaaniApp/devices.html', context)

# for url devices/attachments/:id
@api_view(['GET', 'PUT', 'DELETE'])
@require_auth
def attachments_rest(request, attachment_id):
    if request.method == 'GET':
        return _read(request, attachment_id)
    if request.method == 'PUT':
        return _update(request, attachment_id)
    if request.method == 'DELETE':
        return _delete(request, attachment_id)

# for url devices/attachments
@api_view(['GET', 'POST'])
@require_auth
def attachments_rest_root(request):
    if request.method == 'POST':
        return _create(request) 
    if request.method == 'GET':
        return _list(request)

# GET /devices/attachments/:id
def _read(request, attachment_id):
    response = _responseBase()

    try:
        attachment = DeviceIndividual.get(attachment_id)
    except Exception as e:
        _add_error(response, repr(e))
        _logError(e)
        return JsonResponse(response)

    response['data'] = attachment
    return JsonResponse(response)

# PUT devices/attachments/:id
def _update(request, attachment_id):
    response = _responseBase();

    attachment = _get_subdict(QueryDict(request.body).dict(),
        ['individualID', 'deviceID', 'attached', 'removed', 'id'])
    try:
        DeviceIndividual.update(**attachment)
    except Exception as e:
        _add_error(response, repr(e))
        _logError(e)
        return JsonResponse(response)

    response['data'] = attachment
    return JsonResponse(response)

# DELETE devices/attachments/:id
def _delete(request, attachment_id):
    response = _responseBase()

    try:
        DeviceIndividual.delete(attachment_id)
    except Exception as e:
        _add_error(response, repr(e))
        _logError(e)
        return JsonResponse(response)

    return JsonResponse(response)

# GET /devices/attachments
def _list(request):
    response = _responseBase()

    try:
        attachments = DeviceIndividual.find(**request.GET.dict())
    except Exception as e:
        _add_error(response, repr(e))
        _logError(e)
        return JsonResponse(response)

    response['data'] = attachments
    return JsonResponse(response)

# POST /devices/attachments
def _create(request):
    response = _responseBase()

    try: 
        opts = _get_subdict(request.POST.dict(), 
            ['individualID', 'deviceID', 'attached', 'removed'])
        attachment = DeviceIndividual.create(**opts)
    except Exception as e:
        if isinstance(e, AlreadyHasDevice):
            response['status'] = 'REFUSE'
            conflictingDevID = e.deviceIDs[0]
            name = device.get(conflictingDevID).deviceManufacturerID
            response['message'] = \
                _("Annettuna aikana linnussa on jo kiinni laite %s" % name)
        elif isinstance(e, DeviceAlreadyAttached):
            response['status'] = 'REFUSE'
            conflictingIndID = e.individualIDs[0]
            name = individual.get(conflictingIndID).nickname
            response['message'] = \
                _("Annettuna aikana laite on jo kiinni linnussa %s" % name) 
        else:
            _logError(e) 
            _add_error(response, repr(e))
        return JsonResponse(response)

    response['data'] = attachment
    return JsonResponse(response)


def _add_error(response, error):
    response['errors'].append(error)
    response['status'] = 'ERROR'

def _logError(err):
    s = '\n---- BEGIN LOGGED EXCEPTION ----\n\n'
    s += _stringify_error(err)
    s += '\n---- END LOGGED EXCEPTION ----\n'
    logger.error(s)

def _stringify_error(err):
    return '\n'.join(traceback.format_exception(None, err, None))

def _get_subdict(dct, keys):
    return { k:dct[k] for k in dct if k in keys and dct[k] }
    
