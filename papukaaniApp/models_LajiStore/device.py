from papukaaniApp.services.lajistore_service import LajiStoreAPI
from papukaaniApp.utils.model_utils import *


class Device:
    '''
    Represents the Device table of LajiStore
    '''

    def __init__(self, deviceId, deviceType, deviceManufacturer, createdAt, lastModifiedAt,
                 facts=None, individuals=None, id=None, **kwargs):
        self.id = id
        self.deviceId = deviceId
        self.deviceType = deviceType
        self.deviceManufacturer = deviceManufacturer
        self.createdAt = createdAt
        self.lastModifiedAt = lastModifiedAt
        self.facts = facts
        self.individuals = individuals

        if not facts:
            self.facts = [{"name": "status", "value": "not attached"}]

        if len(self.facts) == 0:
            self.facts = [{"name":"status", "value":"not attached"}]

        if not individuals:
            self.individuals = []

    def delete(self):
        '''
        Deletes the device from LajiStore. Note that the object is not destroyed!
        '''
        LajiStoreAPI.delete_device(self.id)

    def update(self):
        '''
        Saves changes to the object to the corresponding LajiStore entry.
        '''
        self.lastModifiedAt = current_time_as_lajistore_timestamp()
        LajiStoreAPI.update_device(**self.__dict__)  # __dict__ puts all arguments here

    def attach_to(self, individual, timestamp):
        '''
        Attaches this device to an individual. Previously attached device will be removed.
        '''
        if self.facts[0]["value"] == "not attached":
            self.individuals.append({
                "individualId": individual.individualId,
                "attached": timestamp,
                "removed": None
            })
            self.change_status()
            return True
        return False

    def detach_from(self, individual, timestamp):
        '''
        Removes this device from an individual. If the individual is already removed, old removal date will be rewritten.
        '''
        for indiv in self.individuals:
            if indiv["individualId"] == individual.individualId and indiv["removed"] is None:
                indiv["removed"] = timestamp
        self.change_status()

    def change_status(self):
        '''
        Changes the status of the device to attached if not attached and vice versa.
        '''
        self.facts[0]["value"] = "attached" if self.facts[0]["value"] == "not attached" else "not attached"


def find(**kwargs):
    '''
    Find all matching devices.
    :param kwargs: Search parameters.
    :return: A list of Device objects.
    '''
    return _get_many(**kwargs)


def get_all():
    '''
    Returns all devices
    :return A list of Device objects:
    '''
    return _get_many()


def get_or_create(deviceId, parserInfo):
    '''
    Gets the device with the given deviceId, or creates it if not found.
    :return: a Device object
    '''
    result = find(deviceId=deviceId)
    if len(result) == 0:
        return create(
            deviceId=deviceId,
            deviceType=parserInfo["type"],
            deviceManufacturer=parserInfo["manufacturer"],
            createdAt=current_time_as_lajistore_timestamp(),
            lastModifiedAt=current_time_as_lajistore_timestamp(),
            facts=[]
        )
    else:
        return result[0]


def get(id):
    '''
    Gets a device from LajiStore
    :param id: The LajiStore ID of the device
    :return: A Device object
    '''
    device = LajiStoreAPI.get_device(id)
    return Device(**device)


def create(deviceId, deviceType, deviceManufacturer, createdAt, lastModifiedAt, facts):
    '''
    Creates a device instance in LajiStore and a corresponding Device object
    :return: A Device object
    '''
    device = Device(deviceId, deviceType, deviceManufacturer, createdAt, lastModifiedAt, facts)
    data = LajiStoreAPI.post_device(**device.__dict__)
    device.id = data["id"]

    return device


def delete_all():
    '''
    Deletes all devices. Can only be used in test enviroment.
    '''
    LajiStoreAPI.delete_all_devices()


def _get_many(**kwargs):
    data = LajiStoreAPI.get_all_devices(**kwargs)
    devices = []
    for device in data:  # creates a list of devices to return
        devices.append(Device(**device))
    return devices
