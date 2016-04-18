from django.core.cache import caches
from papukaaniApp.models_TipuApi import species
from django.views.decorators.clickjacking import xframe_options_exempt
from papukaaniApp.models_LajiStore import *
from papukaaniApp.views.login_view import *
from papukaaniApp.views.decorators import count_lajistore_requests


@count_lajistore_requests
@xframe_options_exempt  # Allows the view to be loaded in an iFrame
def public(request):
    """
    Controller for '/public/'.
    """

    authorized = authenticated(request)

    public_cache = False
    individual_cache = None
    species_cache = None

    if not authorized:  # try to load cache for non-loggedIn users
        try:
            public_cache = caches['public']
            individual_cache = public_cache.get('individuals_' + request.LANGUAGE_CODE)
            species_cache = public_cache.get('species_' + request.LANGUAGE_CODE)
        except:
            pass

    if individual_cache is None or species_cache is None: # load from datastore
        individuals = _get_individuals(request)
        ordered_species = _get_species(request, individuals)
        if public_cache: # if using cache, set values
            public_cache.set_many({
                'individuals_' + request.LANGUAGE_CODE: individuals,
                'species_' + request.LANGUAGE_CODE: ordered_species
            })
    else: # use cache
        individuals = individual_cache
        ordered_species = species_cache

    if public_cache:
        public_cache.close()

    extended = 'base.html'
    if authorized:
        extended = 'base_with_nav.html'

    context = {'individuals': json.dumps(individuals),
               'species': json.dumps(ordered_species),
               'display_navigation': authorized,
               'individualIds': request.GET.get('individuals', []),
               'speed': request.GET.get('speed', ''),
               'loc': request.GET.get('loc', [61.0, 20.0]),
               'zoom': request.GET.get('zoom', 5),
               'start_time': request.GET.get('start_time', ''),
               'end_time': request.GET.get('end_time', ''),
               'extended': extended,
               'page_id': 'public'
               }

    return render(request, 'papukaaniApp/public.html', context)


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    return obj.__dict__


def _get_individuals(request):
    individuals = dict()
    inds_objects = individual.find_exclude_deleted()
    for individuale in inds_objects:
        key = individuale.taxon
        individuals.setdefault(key, [])
        individualInfo = {'nickname': individuale.nickname,
                          'description': individuale.description,
                          'descriptionURL': individuale.descriptionURL,
                          'news': json.dumps(news.find_by_individual_and_language(individualID=individuale.id,
                                                                                  language=request.LANGUAGE_CODE),
                                             default=set_default)
                          }

        individuals[key].append({individuale.id: individualInfo})
    return individuals


def _get_species(request, individuals, cache=False):
    all_species = species.get_all_in_user_language(request.LANGUAGE_CODE)
    ordered_species = []
    for s in all_species:
        if s.id in individuals:
            individuals[s.name] = individuals.pop(s.id)  # Renames the species
            ordered_species.append(s.name)
    ordered_species.sort()
    return ordered_species
