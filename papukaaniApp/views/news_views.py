from  papukaaniApp.services.laji_auth_service.require_auth import require_auth
from django.shortcuts import render
from papukaaniApp.models_LajiStore import individual
from papukaaniApp.models_TipuApi import species
from papukaaniApp.views.decorators import count_lajistore_requests
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _


@count_lajistore_requests
@require_auth
def news(request):
    """
    Controller for '/news/'. GET renders view
    """
    context = {
        'test': "testi"
    }
    return render(request, 'papukaaniApp/news.html', context)
