from django.shortcuts import render, redirect
from papukaaniApp.models import GeneralParser
from  papukaaniApp.services.laji_auth_service.require_auth import require_auth
from django.core import serializers
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
        except:
            raise ValueError("POST request does not contain required parameters!")


    return render(request, 'papukaaniApp/formats.html')

def list_formats(request):
    parsers = GeneralParser.objects.all()
    return render(request, "papukaaniApp/list_formats.html", context={"formats" : parsers})


def show_format(request, id):
    parser = GeneralParser.objects.get(id=id)

    if request.method == 'GET':
        return render(request, "papukaaniApp/show_format.html", context={"format" : parser})

    if request.method == 'POST':
        data = request.POST.copy().dict()
        data.pop("csrfmiddlewaretoken")

        try:
            for param in data:
                setattr(parser, param, data[param])
            parser.save()
            messages.add_message(request, messages.SUCCESS, "Muutokset tallennettu!")
        except:
            messages.add_message(request, messages.ERROR, "Jokin meni pieleen!")
            return redirect(show_format)

        return redirect(list_formats)


def delete_format(request, id):
    GeneralParser.objects.get(id=id).delete()

    return redirect(list_formats)

