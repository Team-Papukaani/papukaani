from rest_framework.decorators import api_view
from rest_framework.response import Response
from papukaaniApp.models_LajiStore import document, individual, gathering
from datetime import datetime


@api_view(['GET'])
def getGatheringsForDevice(request):
    """
    Django REST-interface controller for getting device-specific (devId request parameter) documents.
    :return: List of documents that match the deviceId.
    """
    docs = document.find(deviceID=request.GET.get('devId'))
    doc = docs[0].gatherings if len(docs) > 0 else []
    gatherings = [g.to_lajistore_json() for g in doc]
    for g in gatherings:
        _move_altitude(g)
    return Response(gatherings)


@api_view(['GET'])
def getGatheringsForIndividual(request):
    """
    REST-controller for getting bird-specific gatherings.
    :param request:
    :return: A List of gatherings related to the bird, with the bird's nickname appended to the end.
    """

    ids = request.GET.get('individualId').split(",")
    data = {}
    for id in ids:
        indiv = individual.get(id)
        gatherings = [g.to_lajistore_json() for g in indiv.get_gatherings()]
        for g in gatherings:
            _remove_unwanted_info_from_gathering(g)
            _move_altitude(g)
        gatherings.append(indiv.nickname)
        data[id] = gatherings
    return Response(data)


def _remove_unwanted_info_from_gathering(gathering):
    """
    Removes any unwanted information from the gathering before sending.
    :param gathering: Gathering to be processed.
    :return: Gathering containing only necessary information.
    """
    if 'publicityRestrictions' in gathering:
        del gathering['publicityRestrictions']


def _move_altitude(g):
    coordinates = g['wgs84Geometry']['coordinates']
    if len(coordinates) == 3:
        g['altitude'] = coordinates.pop()
