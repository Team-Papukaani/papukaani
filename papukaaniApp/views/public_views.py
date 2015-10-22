import json

from django.shortcuts import render, get_object_or_404

from papukaaniApp.models import *
from papukaaniApp.utils.view_utils import extract_latlongs
from django.views.decorators.clickjacking import xframe_options_exempt
from papukaaniApp.models_LajiStore import *

@xframe_options_exempt  #Allows the view to be loaded in an iFrame
def public(request):
    """
    Controller for '/public/'.
    """

    docs = [d.to_dict() for d in document.get_all()]

    return render(request, 'papukaaniApp/public.html', {"docs": json.dumps(docs)})



