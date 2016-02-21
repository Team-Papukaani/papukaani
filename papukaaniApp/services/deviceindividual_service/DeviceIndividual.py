from papukaaniApp.services.lajistore_service import LajiStoreAPI

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
    if get_attached_individual(deviceID) is None:
        if get_attached_device(individualID) is None:
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


def get_attached_individual(deviceID):
    '''
        Return currently attached individuals id or None for not currently attached
        :return: ID or None
    '''
    attachments = get_individuals_for_device(deviceID)
    for attachment in attachments:
        if attachment["removed"] is None:
            return attachment
    return None

def get_attached_device(individualID):
    '''
        Return currently attached devices id or None for not currently attached
        :return: ID or None
    '''
    attachments = get_devices_for_individual(individualID)
    for attachment in attachments:
        if attachment["removed"] is None:
            return attachment
    return None


def get_devices_for_individual(individualID):
    '''
        Return all attached devices for individual
        :return: List of attachments
    '''
    individualID = '"' + _URL + _INDIVIDUAL_PATH + "/" + individualID + '"'
    return find(individualID=individualID)


def get_individuals_for_device(deviceID):
    '''
        Return all attached inviduals for device
        :return: List of attachments
    '''
    deviceID = '"' + _URL + _DEVICE_PATH + "/" + deviceID + '"'
    return find(deviceID=deviceID)


def find(**kwargs):
    attachments = LajiStoreAPI.get_all_deviceindividual(**kwargs)

    devices = LajiStoreAPI.get_all_devices()
    deviceIDs = set()
    for device in devices:
        deviceIDs.add(device['id'])

    individuals = LajiStoreAPI.get_all_individuals()
    individualIDs = set()
    for individual in individuals:
        if not individual['deleted'] == True:
            individualIDs.add(individual['id'])

    unsynced = []

    for attachment in attachments:
        if not attachment['deviceID'] in deviceIDs or not attachment['individualID'] in individualIDs:
            unsynced.append(attachment)

        elif "removed" not in attachment:
            attachment["removed"] = None

    attachments = list([attachment for attachment in attachments if attachment not in unsynced])
    return attachments

def delete_all():
    '''
    Deletes all DeviceIndividuals. Can only be used in test enviroment.
    '''
    LajiStoreAPI.delete_all_deviceindividual()