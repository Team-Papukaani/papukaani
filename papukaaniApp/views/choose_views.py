import datetime
from papukaaniApp.utils.view_utils import *
from papukaaniApp.models import MapPoint
from django.shortcuts import render, redirect
from django.db.transaction import atomic
from papukaaniApp.models_LajiStore import gathering, document
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
        docs = [d.to_dict() for d in document.get_all()]
        return render(request, 'choose.html', {'points': json.dumps(docs)})


def _set_points_public(request):
    docs = json.loads(request.POST['data'])
    for dict in docs:
        document.update_from_dict(**dict)
