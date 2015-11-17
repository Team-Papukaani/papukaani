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
def getCoordinatesForDeviceByTime(request):
    latlngs = []
    start = datetime.strptime(request.GET.get('start'), "%d-%m-%YT%H:%M 00:00")
    end = datetime.strptime(request.GET.get('end'), "%d-%m-%YT%H:%M 00:00")
    print(end)
    docs = [d.to_dict() for d in document.find(deviceId=request.GET.get('devId'))]
    for doc in docs:
        gatherings = doc['gatherings']
        for g in gatherings:
            if start <= datetime.strptime(g['timeStart'], "%Y-%m-%dT%H:%M:%S+00:00") <= end:
                latlng = g['wgs84Geometry']
                latlngs.append(latlng['coordinates'])
    return Response(latlngs)