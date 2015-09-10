from django.shortcuts import render, redirect
from django.core.serializers import serialize
##from .models import MapPoint

def index(request):
    return render(request, 'index.html')

def public(request):
    return render(request, 'public.html')

def upload(request):
    if request.method == 'POST':
        file =request.FILES['file'].read()
        data = []
        ##data = parse(file)
        points = []
        #for point in data:
            ##points.append(MapPoint.objects.create(test="test"))

        return render(request, 'index.html', {'points' : serialize('json', points)})



    return redirect(index)