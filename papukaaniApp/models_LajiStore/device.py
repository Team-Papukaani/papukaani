from papukaaniApp.services.lajistore_service import LajiStoreAPI


class Device:
    def __init__(self, id, device_id, device, device_type, device_manufacturer, created_at, created_by,
                 last_modified_at, last_modified_by, facts, **kwargs):
        self.id = id
        self.deviceId = device_id
        self.device = device
        self.deviceType = device_type
        self.deviceManufacturer = device_manufacturer
        self.createdAt = created_at
        self.createdBy = created_by
        self.lastModifiedAt = last_modified_at
        self.lastModifiedBy = last_modified_by
        self.facts = facts

    def delete(self):
        LajiStoreAPI.delete_device(self.id)

    def update(self):
        LajiStoreAPI.update_device(**self.__dict__)  # __dict__ puts all arguments here


def find(**kwargs):
    return _get_many(**kwargs)


def get_all():
    return _get_many()


def get(device_id):
    device = LajiStoreAPI.get_device(device_id)
    return Device(**device)


def create(device_id, device_type, device_manufacturer, created_at, created_by, last_modified_at, last_modified_by,
           facts):
    device = LajiStoreAPI.post_device(device_id, device_type, device_manufacturer, created_at, created_by,
                                      last_modified_at, last_modified_by, facts)
    return Device(**device)


def _get_many(**kwargs):
    data = LajiStoreAPI.get_all_devices(**kwargs)
    devices = []
    for device in data:  # creates a list of devices to return
        devices.append(Device(**device))
    return devices
