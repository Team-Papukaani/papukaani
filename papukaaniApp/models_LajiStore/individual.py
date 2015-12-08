from papukaaniApp.services.lajistore_service import LajiStoreAPI
from . import device, document
from papukaaniApp.utils.model_utils import current_time_as_lajistore_timestamp

class Individual:
    '''
    Represents the Individual table of LajiStore
    '''

    def __init__(self, individualId, taxon, id=None, deleted="", facts=None, **kwargs):
        self.id = id
        self.individualId = individualId
        self.taxon = taxon
        self.deleted = deleted
        self.facts = facts

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
        self.lastModifiedAt = current_time_as_lajistore_timestamp()
        LajiStoreAPI.update_individual(**self.__dict__)  # __dict__ puts all arguments here

    def get_gatherings(self):
        '''
        Get all public gatherings related to this individual.
        :return: a list of gatherings
        '''
        devices = []
        for d in device.get_all():
            if self.individualId in [i["individualId"] for i in d.individuals  if "individualId" in i]:
                devices.append(d)

        docs = []
        for d in devices:
            timeranges = [(i["attached"], i["removed"] if i["removed"] else "*") for i in d.individuals if i["individualId"] == self.individualId]
            devices_docs = [document.find(deviceId=d.deviceId, filter={"gatherings_publicity":"public"})[0] for deviceId in devices]

            for dd in devices_docs:
                for doc in docs:
                    if doc.id == dd.id:
                        doc.gatherings += dd.gatherings
                    else:
                        break
                docs.append(dd)

        gatherings = []
        for d in docs: gatherings += d.gatherings

        return gatherings


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
    """
    :param mode: default 1 for ALL, 0 for non-deleted.
    """
    data = LajiStoreAPI.get_all_individuals(**kwargs)
    individuals = []
    for individual in data:  # creates a list of individuals to return
        if mode == 0:
            if 'deleted' not in individual:
                individuals.append(Individual(**individual))
            elif not individual['deleted']:
                individuals.append(Individual(**individual))
        elif mode == 1:
            individuals.append(Individual(**individual))
    return individuals

