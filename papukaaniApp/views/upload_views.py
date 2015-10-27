from papukaaniApp.models import *
from papukaaniApp.utils.parser import *
from django.shortcuts import render
from papukaaniApp.utils.view_utils import *
import json, uuid
from papukaaniApp.models_LajiStore import *
import time
from django.contrib import messages

def upload(request):
    """
    Controller for '/upload/'. GET shows upload screen, POST uploads file.
    Point data is parsed from file and saved to database.
    Point data for Leaflet returned in response.
    """
    if request.method == 'GET':
        return _render_with_message(request)
    if request.method == 'POST':
        if 'file' in request.FILES:

            file = request.FILES['file']
            try:
                data = ecotones_parse(file)

            except:
                messages.add_message(request, messages.ERROR, 'Tiedostosi formaati ei ole kelvollinen!')
                return redirect(upload)
            points = create_points(data)
            return _render_points(points, request)

        messages.add_message(request, messages.ERROR, "Et valinnut ladattavaa tiedostoa!")
        return redirect(upload)

def _render_points(points, request):
    latlongs = [[g.geometry[1], g.geometry[0]] for g in points]
    return render(request, 'upload.html', {'points': json.dumps(latlongs)})


def _render_with_message(request):
    message = request.GET['m'] if 'm' in request.GET else ''
    return render(request, 'upload.html', {"message": message})

