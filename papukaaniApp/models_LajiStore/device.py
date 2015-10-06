from papukaaniApp.services.lajistore_service import LajiStoreAPI

class Device():
    '''
    Represents the Device table of LajiStore
    '''
    def __init__(self, id, deviceId, deviceType, deviceManufacturer, createdAt, createdBy, lastModifiedAt,
                 lastModifiedBy, facts, **kwargs):
        self.id = id
        self.deviceId = deviceId
        self.deviceType = deviceType
        self.deviceManufacturer = deviceManufacturer
        self.createdAt = createdAt
        self.createdBy = createdBy
        self.lastModifiedAt = lastModifiedAt
        self.lastModifiedBy = lastModifiedBy
        self.facts = facts

    def delete(self):
        '''
        Deletes the device from LajiStore. Note that the object is not destroyed!
        '''
        LajiStoreAPI.delete_device(self.id)

    def update(self):
        '''
        Saves changes to the object to the corresponding LajiStore entry.
        '''
        LajiStoreAPI.update_device(**self.__dict__)  # __dict__ puts all arguments here


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


def get(deviceId):
    '''
    Gets a device from LajiStore
    :param id: The LajiStore ID of the device
    :return: A Device object
    '''
    device = LajiStoreAPI.get_device(deviceId)
    return Device(**device)


def create(deviceId, deviceType, deviceManufacturer, createdAt, createdBy, lastModifiedAt, lastModifiedBy, facts):
    '''
    Creates a device instance in LajiStore and a corresponding Device object
    :return: A Device object
    '''
    device = LajiStoreAPI.post_device(deviceId, deviceType, deviceManufacturer, createdAt, createdBy, lastModifiedAt,
                                      lastModifiedBy, facts)
    return Device(**device)


def _get_many(**kwargs):
    data = LajiStoreAPI.get_all_devices(**kwargs)
    devices = []
    for device in data:  # creates a list of devices to return
        devices.append(Device(**device))
    return devices
