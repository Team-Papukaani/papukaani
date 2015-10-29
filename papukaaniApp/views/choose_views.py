import json

from django.shortcuts import render, redirect

from papukaaniApp.utils.view_utils import *
from papukaaniApp.models_LajiStore import device, document


def choose(request):
    """
    Controller for '/choose/'. GET renders view,
    POST receives point publicity data as JSON and saves changes to database.

    JSON format ; {"latlong" : [x,y], "id" : int}
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
        return render(request, 'choose.html', {'devices': json.dumps(devices)})


def _set_points_public(request):
    docs = json.loads(request.POST['data'])
    print(docs)
    for dict in docs:
        document.update_from_dict(**dict)
