from rest_framework.decorators import api_view
from rest_framework.response import Response

from papukaaniApp.models_LajiStore import document
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
def getDocumentsForIndividual(request):
    """
    Get the documents of an individual
    :return: List of documents that match the individualId.
    """
    # Probleema: Haetaan ne devicet, joilla individuals-kentässä kyseinen individual, ja sen aikavälillä haetaan dokumentista pisteet.
    docs = [d.to_dict() for d in document.find(individualId=request.GET.get('devId'))] # HUOMIOIKO PUBLICIN?? WATWAT???
    return Response(docs)