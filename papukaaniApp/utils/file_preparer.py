from papukaaniApp.utils.data_formats import *
import csv


def prepare_file(file, parser, static_gps_number = False):
    """
    Reads the given file and extracts the values of individual events.
    :param file: data file
    :param parser: instance of GeneralParser
    :return: A dictionary containing every event as named values.
    """
    spamReader = csv.reader(file, delimiter=parser.split_mark)
    lines = []
    for line in spamReader:
        lines.append(line)
    return _to_dictionary(lines, parser)



    #with file as f:
    #    lines = [line for line in f]
    #decoded = []
    #split_mark = parser.split_mark
    #coding = parser.coding
    #for line in lines:
    #    decoded.append(line.decode(coding).rstrip().split(split_mark))
    #return _to_dictionary(decoded, parser)

def _to_dictionary(lines, parser):
    #if _is_not_valid_file_type(lines, parser):
    #    raise TypeError("a")
    headers = _rename_attributes(lines, parser)

    parsed = []
    for line in lines[1:]:
        parsed_line = dict(zip(headers, line))
        if "gpsNumber" not in parsed_line:
            parsed_line["gpsNumber"] = 0
        if "temperature" not in parsed_line:
            parsed_line["temperature"] = -373.15
        if "altitude" not in parsed_line:
            parsed_line["altitude"] = -0

        parsed.append(parsed_line)
    return parsed

def _is_not_valid_file_type(lines, parser):
    if "GpsNumber" not in lines[0] and parser.formatName == "ecotone":
        return True

def _rename_attributes(lines, parser):
    headers= lines[0]
    general_attributes = ["gpsTime", "longitude", "latitude", "temperature", "altitude"]
    for attribute in general_attributes:
        for x in range(0, len(headers)):
            if headers[x] == getattr(parser, attribute):
                headers[x] = attribute
    return headers



def parser_Info(parser):
    return {"type": "GMS", "manufacturer" : parser.formatName}