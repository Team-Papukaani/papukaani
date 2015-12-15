from __future__ import absolute_import
from .common import *
import os

SECRET_KEY = os.environ["PAPUKAANI_SECRET_KEY"]

DEBUG = False

ALLOWED_HOSTS += ["*"]

DATABASES = {

    'default': {
        'ENGINE': 'django.db.backends.oracle',
        'NAME': 'oracle.luomus.fi:1521/oracle.luomus.fi',
        'USER': 'satellitti_staging',
        'PASSWORD': os.environ['ORACLE_PASSWORD'],
    }

}
