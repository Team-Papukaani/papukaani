from django.shortcuts import render
from papukaaniApp.models import GeneralParser
from  papukaaniApp.services.laji_auth_service.require_auth import require_auth
from django.contrib import messages

@require_auth
def formats(request):

    if request.method == 'POST':
        try:
            data = request.POST.copy().dict()

            if _check_parser_validity(data):
                messages.add_message(request, messages.ERROR, "Pakollista tietoa puuttuu!")
            else:
                if "csrfmiddlewaretoken" in data:
                    data.pop("csrfmiddlewaretoken")
                GeneralParser.objects.create(**data)
                messages.add_message(request, messages.INFO, "Onnistui!")
        except:
            raise ValueError("POST request does not contain required parameters!")


    return render(request, 'papukaaniApp/formats.html')

def _check_parser_validity(parser):
    print(parser)
    if parser["formatName"] and parser["longitude"] and parser["gpsTime"] and parser["latitude"] and parser["delimiter"]:
        return False
    return True

