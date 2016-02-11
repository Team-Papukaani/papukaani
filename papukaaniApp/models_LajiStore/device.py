from papukaaniApp.services.lajistore_service import LajiStoreAPI
from papukaaniApp.utils.model_utils import *


class Device:
    '''
    Represents the Device table of LajiStore
    '''

    def __init__(self, deviceType, deviceManufacturer, deviceManufacturerID,
                 dateCreated, dateEdited, id=None, **kwargs):

        self.deviceType = deviceType
        self.deviceManufacturer = deviceManufacturer
        self.deviceManufacturerID = deviceManufacturerID
        self.dateCreated = dateCreated
        self.dateEdited = dateEdited
        self.id=id


    def delete(self):
        '''
        Deletes the device from LajiStore. Note that the object is not destroyed!
        '''
        LajiStoreAPI.delete_device(self.id)


    def update(self):
        '''
        Saves changes to the object to the corresponding LajiStore entry.
        '''
        self.dateEdited = current_time_as_lajistore_timestamp()
        LajiStoreAPI.update_device(**self.__dict__)  # __dict__ puts all arguments here.


    def attach_to(self, individual, timestamp):
        '''
        Attaches this device to an individual. Previously attached device will be removed.

        if self.facts[0]["value"] == "not attached":
            self.individuals.append({
                "individualId": individual.individualId,
                "attached": timestamp,
                "removed": None
            })
            self.change_status()
            return True
        return False
        '''


    def detach_from(self, individual, timestamp):
        '''
        Removes this device from an individual. If the individual is already removed, old removal date will be rewritten.

        for indiv in self.individuals:
            if indiv["individualId"] == individual.individualId and indiv["removed"] is None:
                indiv["removed"] = timestamp
        self.change_status()
        '''


def find(**kwargs):
    '''
    Find all matching devices.
    :param kwargs: Search parameters. No parameters will search all devices.
    :return: A list of Device objects.
    '''
    data = LajiStoreAPI.get_all_devices(**kwargs)
    print(data)
    devices = []
    for device in data:  # Creates a list of devices to return
        devices.append(Device(**device))
    return devices


def get(id):
    '''
    Gets a device from LajiStore
    :param id: The LajiStore ID of the device
    :return: A Device object
    '''
    device = LajiStoreAPI.get_device(id)
    return Device(**device)


def create(deviceType, deviceManufacturer, deviceManufacturerID, dateCreated=None, dateEdited=None):
    '''
    Creates a device instance in LajiStore and a corresponding Device object
    :return: A Device object
    '''
    current_time = current_time_as_lajistore_timestamp()

    dateCreated = dateCreated if dateCreated else current_time
    dateEdited = dateEdited if dateEdited else current_time
    device = Device(deviceType, deviceManufacturer, deviceManufacturerID, dateCreated, dateEdited)
    data = LajiStoreAPI.post_device(**device.__dict__)

    id_url = data["@id"]
    device.id = id_url.rsplit('/', 1)[-1]

    return device


def delete_all():
    '''
    Deletes all devices. Can only be used in test enviroment.
    '''
    LajiStoreAPI.delete_all_devices()