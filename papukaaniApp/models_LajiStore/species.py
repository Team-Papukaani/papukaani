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
    Returns all devices
    :return A list of Device objects:
    '''
    data = TipuApiAPI.get_all_species()
    species = []
    for datum in data['species']['species']:  # creates a list of devices to return
        species.append(Species(**datum))
    return species
