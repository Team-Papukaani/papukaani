import chardet
from pprint import pprint
from io import StringIO
import csv
from papukaaniApp.models import GeneralParser



def _uploaded_file_to_filestream(file):
    content = file.read()
    encoding = chardet.detect(content)['encoding']
    content = content.decode(encoding)
    filestream = StringIO(content)
    return filestream


def prepare_file(uploaded_file, parser, static_gps_number=False):
    """
    Reads the given file and extracts the values of individual events.
    :param file: data file
    :param parser: instance of GeneralParser
    :return: A dictionary containing every event as named values.
    """
    filestream = _uploaded_file_to_filestream(uploaded_file).read()
    reader = csv.reader(filestream.splitlines(), delimiter=parser.delimiter)

    results = [row for row in reader]

    lines = []
    for line in results:
        lines.append(line)
    return _to_dictionary(lines, parser, static_gps_number)

def _to_dictionary(lines, parser, static_gps_number = False):
    _check_that_file_is_valid(lines, parser)
    headers = _rename_attributes(lines, parser)

    parsed = []
    for line in lines[1:]:
        parsed_line = dict(zip(headers, line))
        if "gpsNumber" not in parsed_line:
            parsed_line["gpsNumber"] = static_gps_number
        if "temperature" not in parsed_line:
            parsed_line["temperature"] = -273.15
        if "altitude" not in parsed_line:
            parsed_line["altitude"] = 0

        parsed.append(parsed_line)
    return parsed


def _check_that_file_is_valid(lines, parser):
    headers = lines[0]
    assert parser.timestamp in headers or (parser.time in headers and parser.date in headers)
    assert parser.longitude in headers
    assert parser.latitude in headers


def _rename_attributes(lines, parser):
    headers= lines[0]
    general_attributes = GeneralParser.possible_column_names

    for attribute in general_attributes:
        for x in range(0, len(headers)):
            if headers[x] == getattr(parser, attribute):
                headers[x] = attribute
    return headers


def parser_Info(parser):
    return {"type": "GMS", "manufacturer": parser.formatName}
