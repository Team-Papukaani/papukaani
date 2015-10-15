from papukaaniApp.services.lajistore_service import LajiStoreAPI


class Individual:
    '''
    Represents the Individual table of LajiStore
    '''

    def __init__(self, id, individualId, taxon, **kwargs):
        self.id = id
        self.individualId = individualId
        self.taxon = taxon

    def delete(self):
        '''
        Ddeletes the device from LajisStore. Note that the object is not destroyed!
        '''
        LajiStoreAPI.delete_individual(self.id)

    def update(self):
        '''
        Saves changes to the object to the corresponding LajiStore entry
        :return:
        '''
        LajiStoreAPI.update_individual(**self.__dict__)  # __dict__ puts all arguments here


def find(**kwargs):
    '''
    Find all mathing individuals
    :param kwargs: Search parameters
    :return: A list of Individual objects
    '''
    return _get_many(**kwargs)


def get_all():
    '''
    Returns all individuals
    :return: A list of Individual objects
    '''
    return _get_many()


def get(id):
    '''
    Gets a device from LajiStore
    :param id: The LajiStore ID of the individual
    :return: A Individual object
    '''
    individual = LajiStoreAPI.get_individual(id)
    return Individual(**individual)


def create(individualId, taxon):
    '''
    Creates an individual instance in LajiStore and a corresponding Indiviual object
    :param id: The LajiStore ID of the object
    :param taxon: The LajiStore taxon of the object
    :return: An Individual object
    '''
    individual = LajiStoreAPI.post_individual(individualId, taxon)
    return Individual(**individual)

def delete_all():
    '''
    Deletes all individuals. Can only be used in test enviroment.
    '''
    LajiStoreAPI.delete_all_individuals()

def _get_many(**kwargs):
    data = LajiStoreAPI.get_all_individuals(**kwargs)
    individuals = []
    for individual in data:  # creates a list of individuals to return

        individuals.append(Individual(**individual))
    return individuals
