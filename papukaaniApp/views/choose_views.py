from papukaaniApp.utils.view_utils import redirect_with_param
from papukaaniApp.models import MapPoint
from django.shortcuts import render, redirect
import json

def choose(request):
    """
    Controller for '/choose/'. GET renders view,
    POST receives point publicity data as JSON and saves changes to database.
    """
    if request.method == 'POST':
        if 'data' in request.POST:
            points = json.loads(request.POST['data'])
            for point in points:
                mPoint = MapPoint.objects.get(id = point['id'])
                mPoint.public = point['public']
                mPoint.save()

            return redirect_with_param(choose, '?m=Valitut pisteet asetettu julkisiksi!')
        return redirect(choose)
    else:
        return render(request, 'choose.html')
