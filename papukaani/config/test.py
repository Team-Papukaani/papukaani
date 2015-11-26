from __future__ import absolute_import
from .common import *
from papukaani import secret_settings
import os

SECRET_KEY = '098#5x@dnk#)p+kijq(%u@*bsho)*u4mgga1f(u&9*-237z0@j'
DEBUG = True

secret_settings.LAJISTORE_USER = secret_settings.LAJISTORE_UNIT_TEST
secret_settings.LAJISTORE_PASSWORD = secret_settings.LAJISTORE_UNIT_TEST_PASSWORD

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

MOCK_AUTHENTICATION = "Skip"