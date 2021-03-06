from papukaaniApp.services.lajistore_service import LajiStoreAPI
from papukaaniApp.services.deviceindividual_service import DeviceIndividual
from papukaaniApp.utils.model_utils import *


class Device:
    '''
    Represents the Device table of LajiStore
    '''

    def __init__(self, deviceType, deviceManufacturer, deviceManufacturerID,
                 dateCreated, dateEdited, id=None):
        self.deviceType = deviceType
        self.deviceManufacturer = deviceManufacturer
        self.deviceManufacturerID = deviceManufacturerID
        self.dateCreated = dateCreated
        self.dateEdited = dateEdited
        self.id = id

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

    def attach_to(self, individualid, timestamp):
        '''
        Attaches this device to an individual
        '''
        DeviceIndividual.attach(self.id, individualid, timestamp)

    def detach_from(self, individualid, timestamp):
        '''
        Removes this device from an individual
        '''
        DeviceIndividual.detach(self.id, individualid, timestamp)

    def get_attached_individualid(self):
        '''
        Return currently attached individuals id or None for not currently attached
        :return: ID or None
        '''
        attachment = DeviceIndividual.get_active_attachment_of_device(self.id)
        if attachment is None:
            return None
        return attachment['individualID']

    def get_attachments(self):
        return DeviceIndividual.get_attachments_of_device(self.id)

    def is_attached(self):
        return False if self.get_attached_individualid() is None else True

    def to_dict(self):
        dict = self.__dict__.copy()
        return dict


def find(**kwargs):
    '''
    Find all matching devices.
    :param kwargs: Search parameters. No parameters will search all devices.
    :return: A list of Device objects.
    '''
    data = LajiStoreAPI.get_all_devices(**kwargs)
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
    if 'id' in device:
        return Device(**device)

    else:
        return None


def create(deviceType, deviceManufacturer, deviceManufacturerID, dateCreated=None, dateEdited=None):
    '''
    Creates a device instance in LajiStore and a corresponding Device object
    :return: A Device object
    '''
    originaldevice = _find_duplicate(deviceManufacturerID)
    if originaldevice is not None:
        return originaldevice

    current_time = current_time_as_lajistore_timestamp()

    dateCreated = dateCreated if dateCreated else current_time
    dateEdited = dateEdited if dateEdited else current_time
    device = Device(deviceType, deviceManufacturer, deviceManufacturerID, dateCreated, dateEdited)
    data = LajiStoreAPI.post_device(**device.__dict__)

    device.id = data['id']

    return device


def delete_all():
    '''
    Deletes all devices. Can only be used in test enviroment.
    '''
    LajiStoreAPI.delete_all_devices()


def _find_duplicate(deviceManufacturerID):
    devices = find(deviceManufacturerID=deviceManufacturerID)
    if devices:
        return devices[0]
    return None
