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

@gzip_page
@api_view(['GET'])
def getPublicGatheringsForIndividual(request):
    """
    REST-controller for getting bird-specific gatherings.
    """

    ids = request.GET.get('individualId').split(",")
    data = {}
    for id in ids:
        indiv = individual.get(id)
        gatherings = _get_gatherings_data(id, public_only=True, extras_onlymapdata=True)
        gatherings.append(indiv.nickname)
        data[id] = gatherings
    return Response(data)

@api_view(['GET'])
@require_auth
def getAllGatheringsForIndividual(request):
    id = request.GET.get('individualId')
    gatherings = _get_gatherings_data(id, public_only=False,
        extras_originatingDevice=True)   
    return Response(gatherings)

def _get_gatherings_data(individual_id, public_only=True, extras_originatingDevice=False, extras_onlymapdata=False):
    indiv = individual.get(individual_id)
    gatherings_obj = indiv.get_public_gatherings() if public_only else indiv.get_all_gatherings(extras_originatingDevice=extras_originatingDevice)
    gatherings_json = []

    for go in gatherings_obj:
        gj = go.to_lajistore_json()

        _move_altitude(gj)

        if public_only:
            _remove_publicity(gj)

        if extras_onlymapdata:
            gj['x'] = gj['wgs84Geometry']['coordinates'][1]
            gj['y'] = gj['wgs84Geometry']['coordinates'][0]
            del gj['wgs84Geometry']

            gj['d'] = gj['dateBegin']
            del gj['dateBegin']

            gj['t'] = gj['temperature']
            del gj['temperature']

            if 'altitude' in gj:
                gj['a'] = gj['altitude']
                del gj['altitude']

            del gj['higherGeography']
            del gj['country']

        if extras_originatingDevice:
            if not 'extras' in gj:
                gj['extras'] = {}
            gj['extras']['originatingDevice'] = go.extras['originatingDevice']

        gatherings_json.append(gj)

    return gatherings_json


def _remove_publicity(gathering):
    if 'publicityRestrictions' in gathering:
        del gathering['publicityRestrictions']

def _move_altitude(g):
    coordinates = g['wgs84Geometry']['coordinates']
    if len(coordinates) == 3:
        g['altitude'] = coordinates.pop()

