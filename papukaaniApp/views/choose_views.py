import json

from django.shortcuts import render, redirect

from papukaaniApp.utils.view_utils import *
from papukaaniApp.models_LajiStore import device, document
from papukaaniApp.services.laji_auth import require_auth


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
        for item in device.get_all():
            devices.append(item.deviceId)
        if "Dev" in devices:
            devices.remove("Dev")
        devices.sort()
        return render(request, 'choose.html', {'devices': json.dumps(devices)})


def _set_points_public(request):
    docs = json.loads(request.POST['data'])
    for dict in docs:
        document.update_from_dict(**dict)
