from __future__ import absolute_import
from .common import *
from papukaani import secret_settings

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '098#5x@dnk#)p+kijq(%u@*bsho)*u4mgga1f(u&9*-237z0@j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

secret_settings.LAJISTORE_USER = secret_settings.LAJISTORE_TEST
secret_settings.LAJISTORE_PASSWORD = secret_settings.LAJISTORE_TEST_PASSWORD


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

## temp
USE_I18N = True
LANGUAGE_CODE = 'en'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

print('qqqq', USE_I18N)
