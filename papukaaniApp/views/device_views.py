from django.shortcuts import get_object_or_404, render
from papukaaniApp.models_LajiStore import gathering, document, device, individual

def devices(request):

    devices = device.get_all()
    individuals = individual.get_all()

    context = {
        'individuals': individuals,
        'devices': devices
    }

    return render(request, 'papukaaniApp/devices.html', context)