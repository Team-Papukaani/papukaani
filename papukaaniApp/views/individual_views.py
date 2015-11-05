import random
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from papukaaniApp.models_LajiStore import gathering, document, device, individual

def individuals(request):
    """
    Controller for '/individuals/'. GET renders view,
    POST saves created or modified individual to the database
    """
    if request.method == 'POST':
        if 'id' in request.POST and 'modify' in request.POST:
            individuale = individual.get(request.POST.get('id'))
            individuale.taxon = request.POST.get('taxon')
            individuale.update()
        elif 'id' in request.POST and 'delete' in request.POST:
            individuale = individual.get(request.POST.get('id'))
            individuale.delete()
        elif 'taxon' in request.POST:
            individuale = individual.create(random.randint(10000000, 99999999), request.POST.get('taxon'))
            individuale.individualId = individuale.id
            individuale.update()
            # Success message

    individual_list = individual.get_all()

    context = {
        'individuals': individual_list
    }

    return render(request, 'papukaaniApp/individuals.html', context)