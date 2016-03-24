from rest_framework.decorators import api_view
from rest_framework.response import Response
from papukaaniApp.models_LajiStore import document, individual, gathering
from datetime import datetime
from papukaaniApp.services.laji_auth_service.require_auth import require_auth

@api_view(['GET'])
def getGatheringsForDevice(request):
    """
    Django REST-interface controller for getting device-specific (devId request parameter) documents.
    """
    docs = document.find(deviceID=request.GET.get('devId'))
    doc = docs[0].gatherings if len(docs) > 0 else []
    gatherings = [g.to_lajistore_json() for g in doc]
    for g in gatherings:
        _move_altitude(g)
    return Response(gatherings)

@api_view(['GET'])
def getPublicGatheringsForIndividual(request):
    """
    REST-controller for getting bird-specific gatherings.
    """

    ids = request.GET.get('individualId').split(",")
    data = {}
    for id in ids:
        indiv = individual.get(id)
        gatherings = _get_gatherings_data(id, public_only=True)
        gatherings.append(indiv.nickname)
        data[id] = gatherings
    return Response(data)

@api_view(['GET'])
@require_auth
def getAllGatheringsForIndividual(request):
    id = request.GET.get('individualId')
    gatherings = _get_gatherings_data(id, public_only=False)
    return Response(gatherings)

def _get_gatherings_data(individual_id, public_only=True):
    indiv = individual.get(individual_id)
    gs = indiv.get_public_gatherings() if public_only else indiv.get_all_gatherings()
    gatherings = [g.to_lajistore_json() for g in gs]
    for g in gatherings:
        _move_altitude(g)
        if public_only:
            _remove_publicity(g)
    return gatherings


def _remove_publicity(gathering):
    if 'publicityRestrictions' in gathering:
        del gathering['publicityRestrictions']

def _move_altitude(g):
    coordinates = g['wgs84Geometry']['coordinates']
    if len(coordinates) == 3:
        g['altitude'] = coordinates.pop()
