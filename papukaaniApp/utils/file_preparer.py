from papukaaniApp.utils.data_formats import *

def prepare_file(file, format):
    """
    Reads the given file and extracts the values of individual events.
    :param file: data file
    :param format: type of given data, ecotone, for example
    :return: A dictionary containing every event as named values.
    """
    with file as f:
        lines = [line for line in f]
    decoded = []
    split_mark = get_attribute_name(format, "split_mark")
    coding = get_attribute_name(format, "coding")
    for line in lines:
        decoded.append(line.decode(coding).rstrip().split(split_mark))
    return _to_dictionary(decoded, format)


def _to_dictionary(lines, format):
    parsed = []

    if "GpsNumber" not in lines[0] and format == "ecotone":
        raise TypeError("a")

    args = ["gpsNumber", "gpsTime", "longitude", "latitude", "temperature", "altitude"]

    for arg in args:
        for x in range(0, len(lines[0])):
            if lines[0][x] == get_attribute_name(format, arg):
                lines[0][x] = arg




    for line in lines[1:]:
        parsed_line = dict(zip(lines[0], line))

        if "gpsNumber" not in parsed_line:
            parsed_line["gpsNumber"] = 0
        if "temperature" not in parsed_line:
            parsed_line["temperature"] = -373.15
        if "altitude" not in parsed_line    :
            parsed_line["altitude"] = -0


        parsed.append(parsed_line)
    return parsed

def parser_Info(format):
    type = get_attribute_name(format, "type")
    return {"type": type, "manufacturer" : format}