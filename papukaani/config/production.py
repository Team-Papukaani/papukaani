from __future__ import absolute_import
from .common import *
import os

SECRET_KEY = os.environ["PAPUKAANI_SECRET_KEY"]

DEBUG = False

ALLOWED_HOSTS += ["*"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'ltkm',
        'USER': 'satelliitti_staging',
        'PASSWORD': os.environ['ORACLE_PASSWORD'],
        'HOST': 'salkku.it.helsinki.fi',
        'PORT': '1521'
    }
}