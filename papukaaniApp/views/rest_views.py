from rest_framework.decorators import api_view
from rest_framework.response import Response
from papukaaniApp.models_LajiStore import document, individual
from datetime import datetime


@api_view(['GET'])
def getGatheringsForDevice(request):
    """
    Django REST-interface controller for getting device-specific (devId request parameter) documents.
    :return: List of documents that match the deviceId.
    """
    docs = document.find(deviceId=request.GET.get('devId'))
    gatherings = docs[0].gatherings if len(docs)>0 else []

    docs = [g.to_lajistore_json() for g in gatherings]
    return Response(docs)


@api_view(['GET'])
def getGatheringsForIndividual(request):
    '''
    REST-controller for getting bird-specific gatherings.
    :param request:
    :return: A List of gatherings related to the bird.
    '''
    indiv = individual.get(request.GET.get('individualId'))
    gatherings = [g.to_lajistore_json() for g in indiv.get_gatherings()]

    return Response(gatherings)

