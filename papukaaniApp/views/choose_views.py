import json

from django.shortcuts import render

from papukaaniApp.utils.view_utils import *
from papukaaniApp.models_LajiStore import device, document, gathering
from papukaaniApp.services.laji_auth_service.require_auth import require_auth


@require_auth
def choose(request):
    """
    Controller for '/choose/'. GET renders view,
    POST receives point publicity data as JSON and saves changes to database.
    """
    if request.method == 'POST':
        if 'data' in request.POST:
            _set_points_public(request)
            return redirect(choose)
        return redirect(choose)

    else:
        devices = device.find()
        devices.sort(key=lambda x: x.id)
        devices_ = {dev.id: dev.deviceManufacturerID for dev in devices}
        return render(request, 'papukaaniApp/choose.html', {'devices': json.dumps(devices_)})


def _set_points_public(request):
    data = json.loads(request.POST['data'])
    deviceId = data["deviceId"]
    gatherings = data["gatherings"]

    doc = document.find(deviceID=deviceId)[0]

    doc.gatherings = [ gathering.from_lajistore_json(**g) for g in gatherings]
    doc.update()
