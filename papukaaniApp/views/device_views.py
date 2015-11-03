from django.shortcuts import get_object_or_404, render
from papukaaniApp.models_LajiStore import gathering, document, device, individual
import json

def devices(request):

    devices = device.get_all()
    individuals = individual.get_all()

    # individualsOfDevices = {}
    # for device2 in devices:
    #     individualsOfDevices[device2.deviceId] = device2.individuals

    individualsOfDevices = {device2.deviceId: device2.individuals for device2 in devices}

    context = {
        'individuals': individuals,
        'devices': devices,
        'json': json.dumps(individualsOfDevices)
    }

    return render(request, 'papukaaniApp/devices.html', context)