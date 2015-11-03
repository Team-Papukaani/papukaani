from django.shortcuts import get_object_or_404, render
from papukaaniApp.models_LajiStore import gathering, document, device, individual
import json

def devices(request):

    devices = device.get_all()
    individuals = individual.get_all()

    # Directory, where key is deviceId and value is an array of individual data
    individuals_of_devices = {device2.deviceId: device2.individuals for device2 in devices}

    # Directory, where key is individualId and value is it's name (taxon)
    individual_names = {individual2.individualId: individual2.taxon for individual2 in individuals}

    context = {
        'individuals': individuals,
        'devices': devices,
        'device_json': json.dumps(individuals_of_devices),
        'individual_json': json.dumps(individual_names)
    }

    return render(request, 'papukaaniApp/devices.html', context)