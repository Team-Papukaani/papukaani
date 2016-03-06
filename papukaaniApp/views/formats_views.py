from django.shortcuts import render, redirect
from papukaaniApp.models import GeneralParser
from  papukaaniApp.services.laji_auth_service.require_auth import require_auth

from django.core import serializers
from django.contrib import messages

from django.utils.translation import ugettext_lazy as _

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
            if not _parser_is_valid(data, request):
                return render(request, "papukaaniApp/formats.html")

            if int(id) > 0:
                parser = GeneralParser.objects.get(id=id)
                for param in data:
                    setattr(parser, param, data[param])
                parser.save()
                messages.add_message(request, messages.SUCCESS, _("Muutokset tallennettu!"))
            else:
                GeneralParser.objects.create(**data)
                messages.add_message(request, messages.SUCCESS, _("Formaatti tallennettu!"))
        except:
            messages.add_message(request, messages.ERROR, _("Jokin meni pieleen."))
            return redirect(list_formats)

        return redirect(list_formats)

    return render(request, "papukaaniApp/formats.html")



@require_auth
def delete_format(request, id):
    GeneralParser.objects.get(id=id).delete()

    return redirect(list_formats)


def _parser_is_valid(parser, request):
    success = True
    if not parser["formatName"]:
        messages.add_message(request, messages.ERROR, _("Formaatin nimi puuttuu."))
        success = False
    if not parser["longitude"]:
        messages.add_message(request, messages.ERROR, _("Longitudi puuttuu."))
        success = False
    if not parser["latitude"]:
        success = False
        messages.add_message(request, messages.ERROR, _("Latitudi puuttuu."))
    if not parser["timestamp"]:
        messages.add_message(request, messages.ERROR, _("Täytä joko aikaleima-kenttä tai kellonaika- ja päivämäärä-kentät."))
        if not parser["time"] or not parser["date"]:
            success = False
    return success


