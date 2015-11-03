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
        doc_array = document.find(deviceId=k)
        points += collections[k]
        if len(doc_array) == 0:
            document.create(str(uuid.uuid4()), collections[k], k)
        else:
            _append_points(doc_array[0].gatherings, collections[k])

            # old      doc_array[0].gatherings += collections[k]

            if len(doc_array) > 1:  # if LajiStore contains redundant documents (more than one document for one device)
                for i in range(1, len(doc_array)):
                    doc_array[0].gatherings += doc_array[i].gatherings  # append points from redundant into first document
                    doc_array[i].delete()  # delete redundant document

            doc_array[0].update()

    return points

def _append_points(LajiStore_gatherings, new_gatherings):
    hashed_gathering = []
    for g in LajiStore_gatherings
        hashed_gatheringg.



