from rest_framework.decorators import api_view
from rest_framework.response import Response
from papukaaniApp.models_LajiStore import document, individual
from datetime import datetime


@api_view(['GET'])
def getDocumentsForDevice(request):
    """
    Django REST-interface controller for getting device-specific (devId request parameter) documents.
    :return: List of documents that match the deviceId.
    """
    docs = [d.to_dict() for d in document.find(deviceId=request.GET.get('devId'))]
    return Response(docs)


@api_view(['GET'])
def getPublicDocumentsForBird(request):
    '''
    REST-controller for getting bird-specific gatherings.
    :param request:
    :return: A List of gatherings related to the bird.
    '''
    indiv = individual.get(request.GET.get('individualId'))
    docs = [d.to_dict() for d in indiv.get_gatherings()]

    return Response(docs)

