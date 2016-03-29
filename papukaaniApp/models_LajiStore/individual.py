from papukaaniApp.services.lajistore_service import LajiStoreAPI
from papukaaniApp.services.deviceindividual_service import DeviceIndividual
from . import device, document, gathering
from papukaaniApp.utils.model_utils import current_time_as_lajistore_timestamp
from datetime import time, datetime
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

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

    def set_gatherings(self, new_gatherings):
        totime = _timestamp_to_datetime
        atts = DeviceIndividual.get_attachments_of_individual(self.id)

        for a in atts:
            start = totime(a['attached'])
            end = totime(a['removed']) if ('removed' in a and a['removed']) else timezone.now()

            doc = document.find(deviceID=a['deviceID'])[0]

            relevant_new_gatherings = [g for g in new_gatherings if 
                    (start <= totime(g['dateBegin']) <= end) and
                    g['extras']['originatingDevice'] == a['deviceID']]

            relevant_old_gatherings = [g for g in doc.gatherings if
                    (start <= totime(g.dateBegin) <= end)]

            # nothing to update?
            if (not relevant_new_gatherings) and (not relevant_old_gatherings):
                continue

            if len(relevant_new_gatherings) != len(relevant_old_gatherings):
                logger.warn('number of old gatherings different from number of new gatherings in choose/setIndividualGatherings. old: %d, new: %d' % 
                    (len(relevant_new_gatherings), len(relevant_old_gatherings)))

            # remove old gatherings
            for g in reversed(doc.gatherings):
                if g in relevant_old_gatherings:
                    doc.gatherings.remove(g)

            # insert new gatherings
            doc.gatherings += [
                gathering.from_lajistore_json(**g) for g in relevant_new_gatherings]

            doc.update()

    def get_all_gatherings(self, extras_originatingDevice=False):
        attachments = DeviceIndividual.get_attachments_of_individual(self.id)

        gatherings = []
        for a in attachments:
            timerange = (a["attached"], a["removed"])
            doc = document.find(deviceID=a["deviceID"])[0]
            relevant_gatherings = list(self._filter_gatherings_by_timerange(
                doc.gatherings, timerange))
            for rg in relevant_gatherings:
                if extras_originatingDevice:
                    rg.extras['originatingDevice'] = a['deviceID']
                gatherings.append(rg)

        return gatherings

    def get_public_gatherings(self):
        '''
        Get all public gatherings related to this individual.
        :return: a list of gatherings
        '''
        return [g for g in self.get_all_gatherings()
            if g.publicityRestrictions == "MZ.publicityRestrictionsPublic"]

    def _filter_gatherings_by_timerange(self, gatherings, timerange):
        for g in gatherings:
            start = _timestamp_to_datetime(timerange[0])
            end = _timestamp_to_datetime(timerange[1]) if timerange[1] else timezone.now()
            gBegin = _timestamp_to_datetime(g.dateBegin)
            if (start <= gBegin <= end):
                yield g

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

