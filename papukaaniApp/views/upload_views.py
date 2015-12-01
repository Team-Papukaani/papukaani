from papukaaniApp.models import *
from papukaaniApp.utils.parser import *
from papukaaniApp.utils.file_preparer import *
from django.shortcuts import render
from papukaaniApp.utils.view_utils import *
import json, uuid
import datetime
from django.contrib import messages
from  papukaaniApp.services.laji_auth_service.require_auth import require_auth

@require_auth
def upload(request):
    """
    Controller for '/upload/'. GET shows upload screen, POST uploads file.
    Point data is parsed from file and saved to database.
    Point data for Leaflet returned in response.
    """
    parsers = GeneralParser.objects.all()

    if request.method == 'GET':
        return render(request, 'upload.html', {'parsers': parsers})
    if request.method == 'POST':
        if 'file' in request.FILES:

            uploaded_file = request.FILES['file']
            parser = GeneralParser.objects.filter(formatName=request.POST.get('fileFormat'))[0]

            try:
                if parser.gpsNumber == '':
                    data = prepare_file(uploaded_file, parser, request.POST.get('gpsNumber'))
                else:
                    data = prepare_file(uploaded_file, parser)


            except:
                messages.add_message(request, messages.ERROR, 'Tiedostosi formaatti ei ole kelvollinen!')
                return redirect(upload)
            points = create_points(data, parser, uploaded_file.name, datetime.datetime.now().strftime("%d-%m-%Y, %H:%M:%S"))
            return _render_points(points, parsers, request)

        messages.add_message(request, messages.ERROR, "Et valinnut ladattavaa tiedostoa!")
        return redirect(upload)


def _render_points(points, parsers, request):
    latlongs = [[g.geometry[1], g.geometry[0]] for g in points]
    return render(request, 'upload.html', {'points': json.dumps(latlongs), 'parsers': parsers})
