from django.shortcuts import render
from papukaaniApp.models import GeneralParser
from  papukaaniApp.services.laji_auth_service.require_auth import require_auth
from django.contrib import messages

@require_auth
def formats(request):
    if request.method == 'POST':
        try:
            data = request.POST.copy().dict()
            print(data)

            if "csrfmiddlewaretoken" in data:
                data.pop("csrfmiddlewaretoken")

            GeneralParser.objects.create(**data)
            messages.add_message(request, messages.ERROR, "Onnistui!")
        except:
            messages.add_message(request, messages.ERROR, "Error!!")
            raise ValueError("POST request does not contain required parameters!")


    return render(request, 'papukaaniApp/formats.html')
