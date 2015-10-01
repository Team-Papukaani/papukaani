from papukaaniApp.services.lajistore_service import LajiStoreAPI

class Device():
	def _init_(self, deviceId, device, deviceType, deviceManufacturer, createdAt, createdBy, lastModifiedAt, lastModifiedBy, facts):
		self.deviceID = deviceID
    		self.device =  device
    		self.deviceType = deviceType
    		self.deviceManufacturer = deviceManufacturer
    		self.createdAt = createdAt
    		self.createdBy = createdBy
    		self.lastModifiedAt = lastModifiedAt
    		self.lastModifiedBy = lastModifiedBy
    		self.facts = facts

def all():
	data = LajiStoreAPI.get_all_devices()
	devices = []
	for device in data:
		devices.append(Device(**device))
	return devices
		
