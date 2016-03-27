from django.http import QueryDict
from papukaaniApp.views.decorators import count_lajistore_requests
from papukaaniApp.services.laji_auth_service.require_auth import require_auth
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from papukaaniApp.models_LajiStore import news
from papukaaniApp.models_LajiStore import individual
from papukaaniApp.models_TipuApi import species
import json

_RESPONSE_BASE = {"errors": None, "status": "OK"}


@count_lajistore_requests
@api_view(['GET', 'POST'])
@require_auth
def news_index(request):
    if request.method == 'POST':
        return _create(request)
    return _index(request)


@count_lajistore_requests
@api_view(['GET'])
@require_auth
def news_list(request):
    return _list(request)


@count_lajistore_requests
@api_view(['GET', 'PUT', 'DELETE'])
@require_auth
def news_rest(request, id):
    if request.method == 'PUT':
        return _update(request, id)
    if request.method == 'DELETE':
        return _delete(request, id)
    return _read(request, id)


def _index(request):
    """
    Controller for '/news/'. GET renders view with template
    """
    individuals = dict()
    inds_objects = individual.find_exclude_deleted()
    for individuale in inds_objects:
        key = individuale.taxon
        individuals.setdefault(key, [])
        individuals[key].append({individuale.id: individuale.nickname})

    all_species = species.get_all_in_user_language(request.LANGUAGE_CODE)
    ordered_species = []
    for s in all_species:
        if s.id in individuals:
            individuals[s.name] = individuals.pop(s.id)  # Renames the species
            ordered_species.append(s.name)
    ordered_species.sort()

    context = {'individuals': json.dumps(individuals),
               'species': json.dumps(ordered_species)
               }
    return render(request, 'papukaaniApp/news.html', context)


def _list(request):
    """
    Controller for '/news/list'. GET returns json list of news
    """
    response = _RESPONSE_BASE.copy()
    response["news"] = {}
    for n in news.find():
        response["news"][n.id] = {
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "language": n.language,
            "publishDate": n.publishDate,
            "targets": n.targets
        }
    return Response(response)


def _create(request):
    """
    Controller for '/news/'. POST create new piece of news
    """
    response = _RESPONSE_BASE.copy()
    missing = _check_missing_params(request.POST, 'title', 'language', 'content')
    _add_error(response, missing)
    if _has_errors(response):
        return Response(response)

    publishDate = None if "publishDate" not in request.POST else request.POST["publishDate"]
    targets = None if "targets" not in request.POST else json.loads(request.POST["targets"])

    try:
        n = news.create(request.POST["title"], request.POST["content"], request.POST["language"], publishDate, targets)
    except Exception as e:
        _add_error(response, e)
        return Response(response)

    response["news"] = {}
    response["news"][n.id] = {
        "id": n.id,
        "title": n.title,
        "content": n.content,
        "language": n.language,
        "publishDate": n.publishDate,
        "targets": n.targets
    }

    return Response(response)


def _read(request, id):
    """
    Controller for '/news/:id'. GET news by id
    """
    response = _RESPONSE_BASE.copy()
    n = news.get(id)
    response["news"] = {}
    if n is not None:
        response["news"] = {
            "id": n.id,
            "title": n.title,
            "content": n.content,
            "language": n.language,
            "publishDate": n.publishDate,
            "targets": n.targets
        }
    else:
        _add_error(response, "Not found")
    return Response(response)


def _update(request, id):
    """
    Controller for '/news/:id'. PUT (update) news by id
    """
    response = _RESPONSE_BASE.copy()
    n = news.get(id)
    response["news"] = {}
    if n is None:
        _add_error(response, "Not found")
        return Response(response)

    PUT = QueryDict(request.body)

    missing = _check_missing_params(PUT, 'title', 'language', 'content')
    _add_error(response, missing)
    if _has_errors(response):
        return Response(response)

    n.title = PUT["title"]
    n.language = PUT["language"]
    n.content = PUT["content"]
    n.publishDate = None if "publishDate" not in PUT else PUT["publishDate"]
    n.targets = [] if "targets" not in PUT else json.loads(PUT["targets"])
    n.update()

    response["news"] = {
        "id": n.id,
        "title": n.title,
        "content": n.content,
        "language": n.language,
        "publishDate": n.publishDate,
        "targets": n.targets
    }
    return Response(response)


def _delete(request, id):
    """
    Controller for '/news/:id'. DELETE news by id
    """
    response = _RESPONSE_BASE.copy()
    n = news.get(id)
    if n is not None:
        n.delete()
    else:
        _add_error(response, "Not found" + id)
    return Response(response)


def _check_missing_params(collection, *args):
    missing = []
    for param in args:
        if not param in collection:
            missing.append("Missing parameter: " + str(param))
    return missing


def _add_error(response, error):
    if not error:
        return
    if response["errors"] is None:
        response["errors"] = []
    response["errors"].append(error)
    response["status"] = "ERROR"


def _has_errors(response):
    if response["errors"] is None:
        return False
    return len(response["errors"]) > 0
