

def prepare_file(file, format):
    """
    Reads the given file and extracts the values of individual events.
    :param file: An Ecotone file.
    :return: A dictionary containing every event as named values.
    """
    if format == "ecotone":
        return ecotone(file)
    if format == 'byholm':
        return byholm(file)


def ecotone(file):
    with file as f:
        lines = [line for line in f]
    decoded = []
    for line in lines:
        decoded.append(line.decode("utf-8").rstrip().split(','))
    if "GpsNumber" not in decoded[0]:
        raise TypeError("a")
    return to_dictionary(decoded)

def byholm(file):
    with file as f:
        lines = [line for line in f]
    decoded = []
    for line in lines:
        decoded.append(line.decode("utf-8").rstrip().split('\t'))
    return to_dictionary(decoded)

def to_dictionary(lines):
    parsed = []
    for line in lines[1:]:
        parsed_line = dict(zip(lines[0], line))


        if "GpsNumber" not in parsed_line:
            parsed_line["GpsNumber"] = 0

        if "GPSTime" not in parsed_line:
            parsed_line["GPSTime"] = parsed_line["DateTime"]
            del parsed_line["DateTime"]

        parsed.append(parsed_line)
    return parsed

def parser_Info(format):
    if format == "ecotone":
        return {"type": "GMS", "manufacturer": "Ecotones"}
    if format == "byholm":
        return {"type": "GMS", "manufacturer": "byholm"}