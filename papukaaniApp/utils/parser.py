import uuid
from papukaaniApp.models_LajiStore import gathering, device, document
from papukaaniApp.utils.file_preparer import *
import datetime

def parse_time(time):
    toks = time.split()
    return toks[0] + "T" + toks[1] + "+00:00"

def create_points(data, parser, name_of_file, time):
    """
    Creates a new entry for every Gathering not already in the database.
    :param data: The contents of the uploaded file.
    :return: A list containing all of the Gatherings found in the file.
    """
    collections = {}

    devices = []

    gathering_facts = _gathering_fact_dics(name_of_file, time)

    for point in data:
        GpsNumber = point['gpsNumber']
        if GpsNumber not in collections:
            collections[GpsNumber] = []

        if GpsNumber not in devices:
            device.get_or_create(deviceId=GpsNumber, parserInfo=parser_Info(parser))
            devices.append(GpsNumber)


        collections[GpsNumber].append(
            gathering.Gathering(
                time=parse_time(point['gpsTime']),
                geometry=[float(point["longitude"]), float(point["latitude"])],
                temperature=float(point['temperature']),
                facts = gathering_facts
            ))

    points = []
    print(1)
    for k in collections.keys():
        doc_array = document.find(deviceId=k)
        points += collections[k]
        if len(doc_array) == 0:
            print("2a")
            document.create(str(uuid.uuid4()), collections[k], k)
        else:
            doc_array[0].gatherings = _union_of_gatherings(doc_array[0].gatherings, collections[k])

            if len(doc_array) > 1:  # if LajiStore contains redundant documents (more than one document for one device)
                for i in range(1, len(doc_array)):
                    doc_array[0].gatherings = _union_of_gatherings(doc_array[0].gatherings, doc_array[i].gatherings)
                    # append points from redundant into first document
                    doc_array[i].delete()  # delete redundant document

            print("2b")
            doc_array[0].update()
    return points

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
                g.facts = g.facts + g2.facts
                break

def _gathering_fact_dics(name_of_file, time):
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