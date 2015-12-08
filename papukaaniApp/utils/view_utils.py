from django.shortcuts import redirect


def redirect_with_param(to, param):
    response = redirect(to)
    response['Location'] += param
    return response


def extract_latlongs(points):
    latlongs = [[float(mapPoint.latitude), float(mapPoint.longitude)] for mapPoint in points]
    return latlongs


def populate_facts(list):
    """
    Converts LajiStore facts into attributes for use in templates
    """
    for item in list:
        if item.facts is None:
            continue
        for fact in item.facts:
            setattr(item, fact['name'], fact['value'])