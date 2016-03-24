from papukaaniApp.models import *
from papukaaniApp.utils.parser import *
from papukaaniApp.utils.file_preparer import *
from django.shortcuts import render
from papukaaniApp.utils.view_utils import *
import json, uuid
import datetime
from django.contrib import messages
from  papukaaniApp.services.laji_auth_service.require_auth import require_auth
from django.utils.translation import ugettext_lazy as _
from papukaaniApp.views.decorators import count_lajistore_requests

@count_lajistore_requests
@require_auth
def upload(request):
    """
    Controller for '/upload/'. GET shows upload screen, POST uploads file.
    Point data is parsed from file and saved to database.
    Point data for Leaflet returned in response.
    """
    parsers = GeneralParser.objects.all()

    if request.method == 'GET':
        return render(request, 'papukaaniApp/upload.html', {'parsers': parsers})
    if request.method == 'POST':
        if 'file' in request.FILES:

            uploaded_file = request.FILES['file']

            parser = GeneralParser.objects.filter(formatName=request.POST.get('fileFormat'))[0]

            try:
                if parser.manufacturerID == '':
                    data = prepare_file(uploaded_file, parser, request.POST.get('manufacturerID'))
                else:
                    data = prepare_file(uploaded_file, parser)

            except:
                messages.add_message(request, messages.ERROR, _("Tiedostosi formaatti ei ole kelvollinen!"))
                return redirect(upload)
            _save_file_to_db(uploaded_file, uploaded_file.name)
            points = create_points(data, parser, uploaded_file.name, datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
            messages.add_message(request, messages.INFO, _("Tiedoston lataus onnistui!"))
            return _render_points(points, parsers, request)

        messages.add_message(request, messages.ERROR, _("Et valinnut ladattavaa tiedostoa!"))
        return redirect(upload)


def _render_points(points, parsers, request):
    latlongs = [[g.geometry[1], g.geometry[0]] for g in points]
    return render(request, 'papukaaniApp/upload.html', {'points': json.dumps(latlongs), 'parsers': parsers})

def _save_file_to_db(file, name):
    dbFile = FileStorage.objects.create(file = file,filename=name, uploadTime=datetime.datetime.now())
    dbFile.save()
