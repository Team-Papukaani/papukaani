from papukaaniApp.services.lajistore_service import LajiStoreAPI


class Individual:
    '''
    Represents the Individual table of LajiStore
    '''

    def __init__(self, individualId, taxon, id=None, deleted="", **kwargs):
        self.id = id
        self.individualId = individualId
        self.taxon = taxon
        self.deleted = deleted

    def delete(self):
        '''
        Deletes the individual from LajiStore. Note that the object is not destroyed!
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
    Find all matching individuals
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


def get_all_exclude_deleted():
    '''
    Returns all individuals not marked as deleted
    :return: A list of Individual objects
    '''
    return _get_many(0)


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
    individual = Individual(individualId, taxon)

    data = LajiStoreAPI.post_individual(**individual.__dict__)
    individual.id = data["id"]

    return individual


def delete_all():
    '''
    Deletes all individuals. Can only be used in test enviroment.
    '''
    LajiStoreAPI.delete_all_individuals()


def _get_many(mode=1, **kwargs):
    data = LajiStoreAPI.get_all_individuals(**kwargs)
    individuals = []
    for individual in data:  # creates a list of individuals to return
        if mode == 0 and not individual['deleted']:
                individuals.append(Individual(**individual))
        elif mode == 1:
            individuals.append(Individual(**individual))
    return individuals
