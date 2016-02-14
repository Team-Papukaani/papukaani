from papukaaniApp.services.lajistore_service import LajiStoreAPI
from papukaaniApp.services.deviceindividual_service import DeviceIndividual
from . import device, document
from papukaaniApp.utils.model_utils import current_time_as_lajistore_timestamp
from datetime import time, datetime
from django.utils import timezone


class Individual:
    '''
    Represents the Individual table of LajiStore
    '''

    def __init__(self, nickname, taxon, ringID="", id=None, deleted="", **kwargs):
        self.id = id
        self.nickname = nickname
        self.taxon = taxon
        self.ringID = ringID
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

    def get_gatherings(self):
        '''
        Get all public gatherings related to this individual.
        :return: a list of gatherings
        '''
        devices = DeviceIndividual.get_devices_for_individual(self.id)

        gatherings = []
        for d in devices:
            timeranges = [(d["attached"], d["removed"])]
            docs = document.find(deviceID=d["deviceID"])
            self._filter_gatherings_by_timeranges(docs, gatherings, timeranges)
        return gatherings

    def _filter_gatherings_by_timeranges(self, docs, gatherings, timeranges):
        for doc in docs:
            for g in doc.gatherings:
                for tr in timeranges:
                    if _timestamp_to_datetime(tr[0]) <= _timestamp_to_datetime(g.dateBegin) <= (_timestamp_to_datetime(
                            tr[1]) if tr[1] else timezone.now()) and g.publicityRestrictions == "MZ.publicityRestrictionsPublic":
                        gatherings.append(g)


def _timestamp_to_datetime(timestamp):
    timestamp = timestamp[:-3] + timestamp[-2:]
    return datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")


def find(**kwargs):
    '''
    Find all matching individuals
    :param kwargs: Search parameters
    :return: A list of Individual objects
    '''
    data = LajiStoreAPI.get_all_individuals(**kwargs)
    individuals = []
    for individual in data:  # creates a list of individuals to return
        individuals.append(Individual(**individual))
    return individuals


def find_exclude_deleted():
    '''
    Returns all individuals not marked as deleted
    :return: A list of Individual objects
    '''
    individuals = find()
    for individual in individuals:
        if individual.deleted:
            individuals.remove(individual)
    return individuals


def get(id):
    '''
    Gets a device from LajiStore
    :param id: The LajiStore ID of the individual
    :return: A Individual object
    '''
    individual = LajiStoreAPI.get_individual(id)
    return Individual(**individual)


def create(nickname, taxon):
    '''
    Creates an individual instance in LajiStore and a corresponding Indiviual object
    :param nickname: nickname for the individual
    :param taxon: The LajiStore taxon of the object
    :return: An Individual object
    '''
    individual = Individual(nickname, taxon)
    data = LajiStoreAPI.post_individual(**individual.__dict__)

    individual.id = data['id']

    return individual


def delete_all():
    '''
    Deletes all individuals. Can only be used in test enviroment.
    '''
    LajiStoreAPI.delete_all_individuals()
