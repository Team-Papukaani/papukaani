from papukaaniApp.services.tipuapi_service import TipuApiAPI


class Species:
    '''
    Represents the Species of TipuApi
    '''

    def __init__(self, id, name, **kwargs):
        self.id = id
        self.name = name


def get_all():
    '''
    Returns all species
    :return A list of Species objects:
    '''
    data = TipuApiAPI.get_all_species()
    species = []
    for datum in data['species']['species']:  # creates a list of devices to return
        species.append(Species(**datum))
    return species


def get_all_in_user_language(user_language):
    '''
    Returns all species and sets the name in Finnish
    :return A list of Species objects:
    '''
    all_species = get_all()
    for species in all_species:
        for name in species.name:
            if name['lang'] == user_language.upper():
                species.name = name['content']
                break
    return all_species
