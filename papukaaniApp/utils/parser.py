from papukaaniApp.models_LajiStore import gathering, device, document
from papukaaniApp.utils.file_preparer import *
from dateutil import parser


def parse_time(timestamp):
    time = parser.parse(timestamp, parser.parserinfo(dayfirst=True))
    return time.strftime("%Y-%m-%dT%H:%M:%S+00:00")


def create_points(data, parser, name_of_file, time):
    """
    Creates a new entry for every Gathering not already in the database.
    :param data: The contents of the uploaded file.
    :return: A list containing all of the Gatherings found in the file.
    """

    return _create_gatherings(data, parser)


def _create_gatherings(data, parser):
    collections = {}
    devices = {}
    for point in data:
        manufacturerID = point['manufacturerID']
        deviceID = _manufacturerIDCheck(collections, devices, parser, manufacturerID)
        _create_one_gathering(collections, deviceID, point)
    return _update_gatherings_to_lajiStore(collections)


def _manufacturerIDCheck(collections, devices, parser, manufacturerID):
    if manufacturerID not in devices:
        found = device.find(deviceManufacturerID=manufacturerID)
        if not found:
            dev = device.create(parser_Info(parser)['deviceType'], parser_Info(parser)['deviceManufacturer'], manufacturerID)
        else:
            dev = found[0]
        collections[dev.id] = []
        devices[manufacturerID]=dev.id
    return devices[manufacturerID]


def _create_one_gathering(collections, deviceID, point):
    timestamp = _extract_timestamp(point)
    try:
        gathering = _generate_gathering(point, timestamp)
        collections[deviceID].append(gathering)
    except ValueError:
        pass


def _extract_timestamp(point):
    if 'time' in point.keys() and 'date' in point.keys():
        timestamp = str(point['date']) + " " + str(point['time']) + ":00"
    else:
        timestamp = point['timestamp']
    return parse_time(timestamp)


def _generate_gathering(point, timestamp):
    return gathering.Gathering(
        dateBegin=timestamp,
        geometry=[float(point["longitude"]), float(point["latitude"])],
        altitude=float(point["altitude"]),
        temperature=int(float(point['temperature'])),
    )


def _update_gatherings_to_lajiStore(collections):
    points = []
    for k in collections.keys():
        doc_array = document.find(deviceID=k)
        points += collections[k]
        if len(doc_array) == 0:
            document.create(collections[k], k)
        else:
            doc_array[0].gatherings = _union_of_gatherings(doc_array[0].gatherings, collections[k])
            _check_redundant_lajiStore_documents(doc_array)
            doc_array[0].update()
    return points


def _check_redundant_lajiStore_documents(doc_array):
    if len(doc_array) > 1:  # if LajiStore contains redundant documents (more than one document for one device)
        for i in range(1, len(doc_array)):
            doc_array[0].gatherings = _union_of_gatherings(doc_array[0].gatherings, doc_array[i].gatherings)
            # append points from redundant into first document
            doc_array[i].delete()  # delete redundant document


def _union_of_gatherings(lajiStore_gatherings, new_gatherings):
    """
    unites lists given in parameters using sets
    :param lajiStore_gatherings: list containing gatherings from LajiStore
    :param new_gatherings: list containing gatherings to add
    :return: A list containing all gatherings from both lists excluding duplicates
    """

    new_gatherings = set(new_gatherings)
    lajiStore_gatherings = set(lajiStore_gatherings)
    no_duplicates = new_gatherings.symmetric_difference(lajiStore_gatherings)
    duplicates_from_new_gatherings = new_gatherings.difference(no_duplicates)
    duplicates_from_lajiStore_gatherings = lajiStore_gatherings.difference(no_duplicates)

    _update_duplicates_from_new_gatherings(duplicates_from_lajiStore_gatherings, duplicates_from_new_gatherings)
    return list(set().union(no_duplicates, duplicates_from_new_gatherings))


def _update_duplicates_from_new_gatherings(duplicates_from_lajiStore_gatherings, duplicates_from_new_gatherings):
    for g in duplicates_from_new_gatherings:
        for g2 in duplicates_from_lajiStore_gatherings:
            if g == g2:
                g.publicityRestrictions = g2.publicityRestrictions
                break


def _gathering_fact_dics(name_of_file, time):
    '''
    gathering_facts = []
    fact1 = {}
    fact1["name"] = "filename"
    fact1["value"] = name_of_file
    fact2 = {}
    fact2["name"] = "upload_time"
    fact2["value"] = time
    gathering_facts.append(fact1)
    gathering_facts.append(fact2)
    return gathering_facts
    '''


def _additional_facts(point, oldfacts):
    '''
    Add any desired additional values as facts.
    :param point: Data for the gathering.
    :param oldfacts: The initial facts for the point.
    :return: List with both original and newly added facts.

    facts = oldfacts.copy()
    if "altitude" in point and point["altitude"]:
        fact = dict()
        fact["name"] = "altitude"
        fact["value"] = point["altitude"]
        facts.append(fact)
    return facts
    '''
