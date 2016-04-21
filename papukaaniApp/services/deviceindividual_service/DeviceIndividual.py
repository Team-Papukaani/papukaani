from papukaaniApp.services.lajistore_service import LajiStoreAPI
from django.conf import settings
import logging
from papukaaniApp.utils import model_utils

_URL = settings.LAJISTORE_URL

_DEVICE_PATH = LajiStoreAPI._DEVICE_PATH
_INDIVIDUAL_PATH = LajiStoreAPI._INDIVIDUAL_PATH
_DEVICEINDIVIDUAL_PATH = LajiStoreAPI._DEVICEINDIVIDUAL_PATH

log = logging.getLogger(__name__)


# Service for DeviceIndividual. Used to manage devices relationship to individuals and vice versa

def create(**kwargs):
    validate_or_raise(kwargs)
    attachment = LajiStoreAPI.post_deviceindividual(**kwargs)
    return attachment
    
def update(**kwargs):
    validate_or_raise(kwargs)
    return LajiStoreAPI.update_deviceindividual(**kwargs)

def attach(deviceID, individualID, timestamp):
    '''
    Attach device to individual
    :param deviceID: device.id
    :param individualID:  individual.id
    :param timestamp: time of attachment e.g.'2016-02-11T09:45:58+00:00'
    '''
    return create(
        deviceID=deviceID,
        individualID=individualID,
        attached=timestamp)  

def detach(deviceID, individualID, timestamp):
    '''
    Detach device from individual
    :param deviceID: device.id
    :param individualID: individual.id
    :param timestamp: time of detachment e.g.'2016-02-11T09:45:58+00:00'
    '''
    old = get_active_attachment_of_device(deviceID)
    return update(
            id=old['id'],
            deviceID=deviceID,
            individualID=individualID,
            attached=old['attached'],
            removed=timestamp)

def _filter_attachments_by_timerange(attachments, start, end):
    ret = []
    for att in attachments:
        att_start = att['attached'] 
        if 'removed' in att and att['removed']:
            att_end = att['removed']
        else:
            att_end = model_utils.current_time_as_lajistore_timestamp()
        if model_utils.timestamp_timeranges_overlap((start, end), (att_start, att_end)):
            ret.append(att)
    return ret

def get_attachments_of_device_during_time(deviceID, start, end):
    attachments = get_attachments_of_device(deviceID)
    return _filter_attachments_by_timerange(attachments, start, end)

def get_attachments_of_individual_during_time(individualID, start, end):
    attachments = get_attachments_of_individual(individualID)
    return _filter_attachments_by_timerange(attachments, start, end)

def get_active_attachment_of_device(deviceID):
    attachments = get_attachments_of_device(deviceID)
    for attachment in attachments:
        if attachment["removed"] is None:
            return attachment
    return None

def get_active_attachment_of_individual(individualID):
    attachments = get_attachments_of_individual(individualID)
    for attachment in attachments:
        if attachment["removed"] is None:
            return attachment
    return None

def get_attachments_of_individual(individualID):
    return find(individualID=individualID)

def get_attachments_of_device(deviceID):
    return find(deviceID=deviceID)

def find(**kwargs):

    if 'deviceID' in kwargs:
        kwargs['deviceID'] = '"' + _URL + _DEVICE_PATH + "/" + kwargs['deviceID'] + '"'
    if 'individualID' in kwargs:
        kwargs['individualID'] = '"' + _URL + _INDIVIDUAL_PATH + "/" + kwargs['individualID'] + '"'

    attachments = LajiStoreAPI.get_all_deviceindividual(**kwargs)
    devices = LajiStoreAPI.get_all_devices()
    deviceIDs = set([d["id"] for d in devices])
    individuals = LajiStoreAPI.get_all_individuals()
    individualIDs = set()

    for i in individuals:
        # soft removed?
        if not i["deleted"]:
            individualIDs.add(i["id"])

    valid = []

    for attachment in attachments:
        if "removed" not in attachment:
            attachment["removed"] = None
        # really removed?
        if attachment['deviceID'] in deviceIDs and attachment['individualID'] in individualIDs:
            valid.append(attachment)
    return valid

def get(id):
    attachment = LajiStoreAPI.get_deviceindividual(id)
    return attachment

def delete(id): 
    LajiStoreAPI.delete_deviceindividual(id)

def delete_all():
    '''
    Deletes all DeviceIndividuals. Can only be used in test enviroment.
    '''
    LajiStoreAPI.delete_all_deviceindividual()

def validate_or_raise(att):

    start = att['attached']
    if 'removed' in att and att['removed']:
        end = att['removed']
    else:
        end = model_utils.current_time_as_lajistore_timestamp()

    if model_utils.timestamp_to_datetime(end) < model_utils.timestamp_to_datetime(start):
        raise ValueError

    ind_atts = get_attachments_of_individual_during_time(att['individualID'],
            start, end)
    if 'id' in att and att['id']:
        ind_atts = [a for a in ind_atts if a['id'] != att['id']]
    if len(ind_atts) != 0:
        raise AlreadyHasDevice([a['deviceID'] for a in ind_atts])

    dev_atts = get_attachments_of_device_during_time(att['deviceID'],
            start, end)
    if 'id' in att and att['id']:
        dev_atts = [a for a in dev_atts if a['id'] != att['id']]
    if len(dev_atts) != 0:
        raise DeviceAlreadyAttached([a['individualID'] for a in dev_atts])

    return True

class AlreadyHasDevice(Exception):
    def __init__(self, deviceIDs):
        super(AlreadyHasDevice, self).__init__()
        self.deviceIDs = deviceIDs

class DeviceAlreadyAttached(Exception):
    def __init__(self, individualIDs):
        super(DeviceAlreadyAttached, self).__init__()
        self.individualIDs = individualIDs
