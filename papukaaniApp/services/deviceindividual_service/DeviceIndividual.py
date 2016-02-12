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
    attachments = LajiStoreAPI.get_all_deviceindividual(individualID=individualID, deviceID=deviceID)
    for attachment in attachments:
        if 'removed' not in attachment:
            attachment["removed"] = timestamp
            LajiStoreAPI.update_deviceindividual(**attachment)


def get_attached_individual(deviceID):
    '''
        Return currently attached individuals id or None for not currently attached
        :return: ID or None
    '''
    deviceID = '"' + _URL + _DEVICE_PATH + "/" + deviceID + '"'
    attachments = LajiStoreAPI.get_all_deviceindividual(deviceID=deviceID)
    for attachment in attachments:
        if 'removed' not in attachment:
            return attachment
    return None


def get_devices_for_individual(individualID):
    '''
        Return all attached devices for individual
        :return: ID or None
    '''
    individualID = '"' + _URL + _INDIVIDUAL_PATH + "/" + individualID + '"'
    return LajiStoreAPI.get_all_deviceindividual(individualID=individualID)


def get_individuals_for_device(deviceID):
    '''
        Return all attached inviduals for device
        :return: ID or None
    '''
    deviceID = '"' + _URL + _DEVICE_PATH + "/" + deviceID + '"'
    return LajiStoreAPI.get_all_deviceindividual(deviceID=deviceID)


def find(**kwargs):
    '''
    Return all attachments
    :param kwargs:
    :return:
    '''
    return LajiStoreAPI.get_all_deviceindividual(**kwargs)
