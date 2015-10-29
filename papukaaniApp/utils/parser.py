from datetime import datetime
import csv, tempfile, uuid
from papukaaniApp.models_LajiStore import gathering, device, document
from time import clock

parserInfo = {"type": "GMS", "manufacturer": "Ecotones"}


def ecotones_parse(file):
    """
    Reads the given file and extracts the values of individual events.
    :param file: An Ecotones-format file.
    :return: A dictionary containing every event as named values.
    """
    with file as f:
        lines = [line for line in f]
    headers = lines[0].decode("utf-8").rstrip().split(',')
    if "GpsNumber" not in headers:
        raise TypeError("a")
    parsed = []
    for line in lines[1:]:
        parsed_line = dict(zip(headers, line.decode("utf-8").rstrip().split(',')))
        parsed.append(parsed_line)
    return parsed


def ecotones_parse_time(time):
    toks = time.split()
    return toks[0] + "T" + toks[1] + "+00:00"


def create_points(data):
    """
    Creates a new entry for every Gathering not already in the database.
    :param data: The contents of the uploaded file.
    :return: A list containing all of the Gatherings found in the file.
    :return: A list containing all of the Gatherings found in the file.
    """
    collections = {}

    devices = []

    for point in data:
        GpsNumber = point['GpsNumber']

        if GpsNumber not in collections:
            collections[GpsNumber] = []

        if GpsNumber not in devices:
            device.get_or_create(deviceId=GpsNumber, parserInfo=parserInfo)
            devices.append(GpsNumber)

        collections[GpsNumber].append(
            gathering.Gathering(
                time=ecotones_parse_time(point['GPSTime']),
                geometry=[float(point["Longtitude"]), float(point["Latitude"])],
                temperature=float(point['Temperature'])
            ))

    points = []

    for k in collections.keys():
        doc = document.get(k)
        points += collections[k]
        if(doc == None):
            document.create(str(uuid.uuid4()), collections[k], k)
        else:
            doc.gatherings += collections[k]
            doc.update()


    return points

