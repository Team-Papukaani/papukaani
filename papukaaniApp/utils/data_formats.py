

ecotone = {}
ecotone["gpsNumber"] = "GpsNumber"
ecotone["gpsTime"] = "GPSTime"
ecotone["longitude"] = "Longtitude"
ecotone["latitude"] = "Latitude"
ecotone["altitude"] = "Altitude"
ecotone["temperature"] = "Temperature"
ecotone["type"] = "GMS"
ecotone["manufacturer"] = "manufacturer"
ecotone["split_mark"] = ","
ecotone["coding"] = "utf-8"

byholm = {}
byholm["gpsNumber"] = "gpsNumber"
byholm["gpsTime"] = "DateTime"
byholm["longitude"] = "Longitude_E"
byholm["latitude"] = "Latitude_N"
byholm["altitude"] = "Altitude_m"
byholm["temperature"] = "temperature"
byholm["type"] = "GMS"
byholm["manufacturer"] = "manufacturer"
byholm["split_mark"] = "\t"
byholm["coding"] = "utf-8"

data_formats = {"ecotone" : ecotone, "byholm": byholm}


def get_attribute_name(data_type, value):
    """
    Gives the name of datafield of given parameters
    :param data_type: type of give data, ecotone, for example.
    :param value: name of datafield
    :return: name of given field in given datatype
    """
    type = data_formats[data_type]
    return type[value]