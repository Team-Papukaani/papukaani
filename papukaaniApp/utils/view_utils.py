from django.shortcuts import redirect


def redirect_with_param(to, param):
    response = redirect(to)
    response['Location'] += param
    return response


def extract_latlongs(points):
    latlongs = [[float(mapPoint.latitude), float(mapPoint.longitude)] for mapPoint in points]
    return latlongs
