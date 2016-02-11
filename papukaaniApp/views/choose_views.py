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
        devices = []
        for item in device.find():
            devices.append(item.id)
        if "Dev" in devices:
            devices.remove("Dev")
        devices.sort()
        return render(request, 'papukaaniApp/choose.html', {'devices': json.dumps(devices)})


def _set_points_public(request):
    data = json.loads(request.POST['data'])
    deviceId = data["deviceId"]
    gatherings = data["gatherings"]

    doc = document.find(deviceId=deviceId)[0]

    doc.gatherings = [ gathering.from_lajistore_json(**g) for g in gatherings]
    doc.update()
