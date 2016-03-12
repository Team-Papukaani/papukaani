from papukaaniApp.services.lajistore_service import LajiStoreAPI
from papukaaniApp.models_LajiStore import *
from django.conf import settings

_URL = settings.LAJISTORE_URL

_DEVICE_PATH = LajiStoreAPI._DEVICE_PATH
_INDIVIDUAL_PATH = LajiStoreAPI._INDIVIDUAL_PATH
_DEVICEINDIVIDUAL_PATH = LajiStoreAPI._DEVICEINDIVIDUAL_PATH


# Service for DeviceIndividual. Used to manage devices relationship to individuals and vice versa

def attach(deviceID, individualID, timestamp):
    '''
    Attach device to individual
    :param deviceID: device.id
    :param individualID:  individual.id
    :param timestamp: time of attachment e.g.'2016-02-11T09:45:58+00:00'
    '''
    if get_active_attachment_of_device(deviceID) is None:
        if get_active_attachment_of_individual(individualID) is None:
            LajiStoreAPI.post_deviceindividual(
                deviceID=deviceID,
                individualID=individualID,
                attached=timestamp
            )


def detach(deviceID, individualID, timestamp):
    '''
    Detach device from individual
    :param deviceID: device.id
    :param individualID: individual.id
    :param timestamp: time of detachment e.g.'2016-02-11T09:45:58+00:00'
    '''
    individualID = '"' + _URL + _INDIVIDUAL_PATH + "/" + individualID + '"'
    deviceID = '"' + _URL + _DEVICE_PATH + "/" + deviceID + '"'
    attachments = find(individualID=individualID, deviceID=deviceID)
    for attachment in attachments:
        if attachment["removed"] is None:
            attachment["removed"] = timestamp
            LajiStoreAPI.update_deviceindividual(**attachment)


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
    individualID = '"' + _URL + _INDIVIDUAL_PATH + "/" + individualID + '"'
    return find(individualID=individualID)


def get_attachments_of_device(deviceID):
    deviceID = '"' + _URL + _DEVICE_PATH + "/" + deviceID + '"'
    return find(deviceID=deviceID)


def find(**kwargs):
    attachments = LajiStoreAPI.get_all_deviceindividual(**kwargs)

    devices = device.find()
    deviceIDs = set({d.id for d in devices})
    individuals = individual.find_exclude_deleted()
    individualIDs = set({i.id for i in individuals})

    valid = []

    for attachment in attachments:
        if "removed" not in attachment:
            attachment["removed"] = None
        if attachment['deviceID'] in deviceIDs and attachment['individualID'] in individualIDs:
            valid.append(attachment)
    return valid


def delete_all():
    '''
    Deletes all DeviceIndividuals. Can only be used in test enviroment.
    '''
    LajiStoreAPI.delete_all_deviceindividual()
