from __future__ import absolute_import
from .common import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '098#5x@dnk#)p+kijq(%u@*bsho)*u4mgga1f(u&9*-237z0@j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
