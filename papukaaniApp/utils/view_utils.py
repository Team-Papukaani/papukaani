from django.shortcuts import redirect

ALL_METHOD_NAMES = ['GET', 'HEAD', 'POST', 'PUT', 'DELETE', 'TRACE', 'OPTIONS',
                    'CONNECT', 'PATCH']


def redirect_with_param(to, param):
    response = redirect(to)
    response['Location'] += param
    return response


def extract_latlongs(points):
    latlongs = [[float(mapPoint.latitude), float(mapPoint.longitude)]
                for mapPoint in points]
    return latlongs
