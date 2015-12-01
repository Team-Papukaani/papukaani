import json

from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response


from papukaaniApp.models import *
from papukaaniApp.utils.view_utils import extract_latlongs
from django.views.decorators.clickjacking import xframe_options_exempt
from papukaaniApp.models_LajiStore import *


@xframe_options_exempt  # Allows the view to be loaded in an iFrame
def public(request):
    """
    Controller for '/public/'.
    """

    devices = []
    for item in device.get_all:
        devices.append(item.deviceId)
    devices.sort()
    return render(request, 'papukaaniApp/public.html', {'devices': json.dumps(devices)})


