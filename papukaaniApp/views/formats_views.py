from django.shortcuts import render
from papukaaniApp.models import GeneralParser
from  papukaaniApp.services.laji_auth_service.require_auth import require_auth

@require_auth
def formats(request):
    if request.method == 'POST':
        try:
            data = request.POST.copy()

            if "csrfmiddlewaretoken" in data:
                data.pop("csrfmiddlewaretoken")

            GeneralParser.objects.create(**data)
        except:
            raise ValueError("POST request does not contain required parameters!")


    return render(request, 'papukaaniApp/formats.html')
