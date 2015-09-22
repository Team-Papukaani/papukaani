from papukaaniApp.utils.view_utils import *
from papukaaniApp.models import MapPoint
from django.shortcuts import render, redirect
import json


def choose(request):
    """
    Controller for '/choose/'. GET renders view,
    POST receives point publicity data as JSON and saves changes to database.

    JSON format ; {"latlong" : [x,y], "id" : int}
    """
    if request.method == 'POST':
        if 'data' in request.POST:
            _set_points_public(request)
            return redirect_with_param(choose, '?m=Valitut pisteet asetettu julkisiksi!')

        return redirect(choose)

    else:
        points = [{"latlong" : [float(mapPoint.latitude), float(mapPoint.longitude)] , "id" : mapPoint.id, "public" : mapPoint.public} for mapPoint in MapPoint.objects.all()]
        return render(request, 'choose.html', {'points' : json.dumps(points)})


def _set_points_public(request):
    points = json.loads(request.POST['data'])
    for point in points:
        mPoint = MapPoint.objects.get(id=point['id'])
        mPoint.public = point['public']
        mPoint.save()


