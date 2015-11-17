from rest_framework.decorators import api_view
from rest_framework.response import Response
from papukaaniApp.models_LajiStore import document


@api_view(['GET'])
def getDocumentsForDevice(request):
    """
    Django REST-interface controller for getting device-specific (devId request parameter) documents.
    :return: List of documents that match the deviceId.
    """
    docs = [d.to_dict() for d in document.find(deviceId=request.GET.get('devId'))]
    return Response(docs)


def getCoordinatesForDeviceByTime(request):
    start = request.GET.get('start')
    end = request.GET.get('end')
    docs = []
    for d in document.find(deviceId=request.GET.get('devId')):
        doc = d.to_dict
        time = doc['timestamp']
        if start <= time <= end:
            docs.append([doc['latitude'], doc['longitude']])
    return Response(docs)

