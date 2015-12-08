from papukaaniApp.services.lajistore_service import LajiStoreAPI
from . import device, document
from papukaaniApp.utils.model_utils import current_time_as_lajistore_timestamp
from datetime import time, datetime

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

        gatherings = []
        for d in devices:
            timeranges = [(i["attached"], i["removed"] if i["removed"] else None) for i in d.individuals if i["individualId"] == self.individualId]
            docs = document.find(deviceId=d.deviceId)
            self._filter_gatherings_by_timeranges(docs, gatherings, timeranges)

        return gatherings

    def _filter_gatherings_by_timeranges(self, docs, gatherings, timeranges):
        for doc in docs:
            for g in doc.gatherings:
                for tr in timeranges:
                    if _timestamp_to_datetime(tr[0]) <= _timestamp_to_datetime(g.time) <= (_timestamp_to_datetime(
                            tr[1]) if tr[1] else datetime.now()) and g.publicity == "public":
                        gatherings.append(g)



def _timestamp_to_datetime(timestamp):
    timestamp = timestamp[:-3]+timestamp[-2:]
    return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")


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

