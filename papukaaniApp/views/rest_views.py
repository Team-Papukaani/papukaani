from rest_framework.decorators import api_view
from rest_framework.response import Response

from rest_framework import permissions, renderers, viewsets

from papukaaniApp.utils.view_utils import *
from papukaaniApp.models_LajiStore import device, document


@api_view(['GET'])
def getDocumentsForDevice(request):
    docs = [d.to_dict() for d in document.find(deviceId=request.GET.get('devId'))]
    return Response(docs)
