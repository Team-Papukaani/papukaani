from django.shortcuts import render, redirect
from papukaaniApp.models import GeneralParser
from  papukaaniApp.services.laji_auth_service.require_auth import require_auth

from django.core import serializers
from django.contrib import messages

@require_auth
def list_formats(request):
    parsers = GeneralParser.objects.all()
    return render(request, "papukaaniApp/list_formats.html", context={"formats": parsers})


@require_auth
def show_format(request, id):
    if request.method == 'GET' and int(id) > 0:
        parser = GeneralParser.objects.get(id=id)
        return render(request, "papukaaniApp/formats.html", context={"format": parser})

    if request.method == 'POST':
        data = request.POST.copy().dict()
        if "csrfmiddlewaretoken" in data:
            data.pop("csrfmiddlewaretoken")

        try:
            if not _parser_is_valid(data):
                messages.add_message(request, messages.ERROR, "Pakollista tietoa puuttuu!")
                return render(request, "papukaaniApp/formats.html")

            if int(id) > 0:
                print("koe3")
                parser = GeneralParser.objects.get(id=id)
                for param in data:
                    setattr(parser, param, data[param])
                parser.save()
                messages.add_message(request, messages.SUCCESS, "Muutokset tallennettu!")
            else:
                print(data)
                GeneralParser.objects.create(**data)
                messages.add_message(request, messages.SUCCESS, "Formaatti tallennettu!")
        except:
            messages.add_message(request, messages.ERROR, "Jokin meni pieleen!")
            return redirect(list_formats)

        return redirect(list_formats)

    return render(request, "papukaaniApp/formats.html")



@require_auth
def delete_format(request, id):
    GeneralParser.objects.get(id=id).delete()

    return redirect(list_formats)


def _parser_is_valid(parser):
    if not parser["formatName"]:
        return False
    if not parser["longitude"]:
        return False
    if not parser["latitude"]:
        return False
    if not  parser["delimiter"]:
        return False
    if not parser["timestamp"]:
        if not parser["time"]:
            return False
        if not parser["date"]:
            return True
    return True


