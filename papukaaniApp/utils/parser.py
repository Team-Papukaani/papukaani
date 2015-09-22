from datetime import datetime


def ecotones_parse(file):
    """
    Reads the given file and extracts the values of individual events.
    :param file: An Ecotones-format file.
    :return: A dictionary containing every event as named values.
    """
    entries = []
    with file as f:
        lines = [line for line in f]
    for i in range(1, len(lines)):
        fields = str(lines[i]).split(',')
        alt = fields[15]
        if len(alt) == 0:
            alt = 0
        e_dict = {
                  "gpsNumber": fields[1],
                  "timestamp": parsetime(fields[2]),
                  # "smstime": int(fields[3]),
                  "latitude": float(fields[4]),
                  "longitude": float(fields[5]),
                  # "batteryvoltage": float(fields[6]),
                  # "gpsdescription": fields[7],
                  "altitude": float(alt),
                  "temperature": float(fields[8])
                  # "gpsintervals": fields[9],
                  # "vhftelemetry": float(fields[10]),
                  # "activity":int(fields[11]),
                  # "gmssignal": int(fields[12]),
                  # "n_satellites": int(fields[13]),
                  # "speed_knots": float(fields[14]),
                  # "altitude": int(fields[15]),
                  # "light": int(fields[16]),
                  # "acc_x": float(fields[17]),
                  # "acc_y": float(fields[18]),
                  # "acc_z": float(fields[19])
                  };
        entries.append(e_dict)
    return entries


def parsetime(timestring):
    """
    Converts the GPSTime-value to correct datetime-format.
    :param timestring: The string to be parsed.
    :return: The original string in datetime-format.
    """
    return datetime.strptime(timestring, "%Y-%m-%d %H:%M:%S")
