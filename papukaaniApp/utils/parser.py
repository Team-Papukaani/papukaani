from datetime import datetime
import csv
import tempfile


def ecotones_parse(file):
    """
    Reads the given file and extracts the values of individual events.
    :param file: An Ecotones-format file.
    :return: A dictionary containing every event as named values.
    """
    with file as f:
        lines = [line for line in f]
    headers = lines[0].decode("utf-8").rstrip().split(',')

    parsed = []
    for line in lines[1:]:
        parsed_line = dict(zip(headers, line.decode("utf-8").rstrip().split(',')))
        parsed.append(parsed_line)
    return parsed

