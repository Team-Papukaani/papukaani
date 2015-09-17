from datetime import datetime


def ecotones_parse(file):
    entries = []
    with file as f:
        lines = [line for line in f]
    for i in range(1, len(lines)):
        fields = str(lines[i]).split(',')
        alt = fields[15]
        if len(alt) == 0:
            alt = 0
        e_dict = {"gpsNumber": int(fields[1]),
                  "timestamp": parsetime(fields[2]),
                  "latitude": float(fields[4]),
                  "longitude": float(fields[5]),
                  "altitude": float(alt),
                  "temperature": float(fields[8])};
        entries.append(e_dict)
    return entries


def parsetime(timestring):
    return datetime.strptime(timestring, "%Y-%m-%d %H:%M:%S")
