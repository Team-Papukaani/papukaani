from papukaaniApp.services.lajistore_service import LajiStoreAPI
from papukaaniApp.services.deviceindividual_service import DeviceIndividual
from . import device, document, gathering
from papukaaniApp.utils.model_utils import current_time_as_lajistore_timestamp
from datetime import time, datetime
from django.utils import timezone

class Individual:
    '''
    Represents the Individual table of LajiStore
    '''

    def __init__(self, nickname, taxon, description=None, descriptionURL=None, ringID="", id=None, deleted=False, **kwargs):
        self.id = id
        self.nickname = nickname
        self.taxon = taxon
        self.description = description
        self.descriptionURL = descriptionURL
        self.ringID = ringID
        self.deleted = deleted

    def delete(self):
        '''
        Deletes the individual from LajiStore. Note that the object is not destroyed!
        '''
        LajiStoreAPI.delete_individual(self.id)


    def softdelete(self):
        '''
        Changes individual status to deleted
        '''
        self.deleted = True
        self.update()

    def update(self):
        '''
        Saves changes to the object to the corresponding LajiStore entry
        :return:
        '''
        LajiStoreAPI.update_individual(**self.__dict__)  # __dict__ puts all arguments here

    def change_gatherings(self, new_gatherings):
        atts = DeviceIndividual.get_attachments_of_individual(self.id)

        totime = _timestamp_to_datetime
        new_gatherings.sort(key=lambda g: totime(g['dateBegin']))
        atts.sort(key=lambda a: totime(a['attached']))

        # On each iteration, update one device's document, or update nothing
        for a in atts:
            start = totime(a['attached'])
            end = totime(a['removed']) if ('removed' in a and a['removed']) else timezone.now()
            assert(start <= totime(new_gatherings[0]['dateBegin']))

            relevant_gatherings = []
            while new_gatherings and (start <= totime(new_gatherings[0]['dateBegin']) <= end):
                relevant_gatherings.append(new_gatherings.pop(0))

            if relevant_gatherings:
                doc = document.find(deviceID=a['deviceID'])[0]
                if len(doc.gatherings) != len(relevant_gatherings):
                    logger.warn('number of old gatherings different from number of new gatherings in choose/changeIndividualGatherings!')
                doc.gatherings = [gathering.from_lajistore_json(**g) for g in relevant_gatherings]
                doc.update()

    def get_all_gatherings(self):
        attachments = DeviceIndividual.get_attachments_of_individual(self.id)

        gatherings = []
        for a in attachments:
            timerange = (a["attached"], a["removed"])
            dev_docs = document.find(deviceID=a["deviceID"])
            self._filter_gatherings_by_timerange(dev_docs, timerange, gatherings)
        return gatherings

    def get_public_gatherings(self):
        '''
        Get all public gatherings related to this individual.
        :return: a list of gatherings
        '''
        return [g for g in self.get_all_gatherings()
            if g.publicityRestrictions == "MZ.publicityRestrictionsPublic"]

    def _filter_gatherings_by_timerange(self, docs, timerange, gatherings_accumulator):
        for doc in docs:
            for g in doc.gatherings:
                start = _timestamp_to_datetime(timerange[0])
                end = _timestamp_to_datetime(timerange[1]) if timerange[1] else timezone.now()
                gBegin = _timestamp_to_datetime(g.dateBegin)
                if (start <= gBegin <= end):
                    gatherings_accumulator.append(g)

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
    return find(deleted="false")


def get(id):
    '''
    Gets a device from LajiStore
    :param id: The LajiStore ID of the individual
    :return: A Individual object
    '''
    individual = LajiStoreAPI.get_individual(id)
    return Individual(**individual)


def create(nickname, taxon, description=None, descriptionURL=None):
    '''
    Creates an individual instance in LajiStore and a corresponding Individual object
    :param nickname: nickname for the individual
    :param taxon: The LajiStore taxon of the object
    :return: An Individual object
    '''
    individual = Individual(nickname, taxon, description, descriptionURL)
    data = LajiStoreAPI.post_individual(**individual.__dict__)

    individual.id = data['id']

    return individual


def delete_all():
    '''
    Deletes all individuals. Can only be used in test enviroment.
    '''
    LajiStoreAPI.delete_all_individuals()
