import logging

"""
Django settings for papukaani project.

Generated by 'django-admin startproject' using Django 1.8.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BASE_DIR = os.path.dirname(PROJECT_DIR)

# Quick-start development config - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'papukaaniApp',
    'rest_framework',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'papukaaniApp.middleware.SessionBasedLocaleMiddleware',
    'papukaaniApp.middleware.RequestLoggingMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'papukaani.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'papukaaniApp.services.laji_auth_service.context_processors.auth'
            ],
        },
    },
]

WSGI_APPLICATION = 'papukaani.wsgi.application'

OTHER_ROOT = os.path.join(PROJECT_DIR, 'staticfiles/../staticfiles/other')

OTHER_URL = '/other/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_DIR, '../papukaani/staticfiles'),
    os.path.join(PROJECT_DIR, '../papukaaniApp/static')
)

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ),
    'UNICODE_JSON': True,
}

# Cache
# https://docs.djangoproject.com/en/1.8/topics/cache/
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'DEFAULT_CACHE_TABLE',
        'OPTIONS': {
            'TIMEOUT': 5 * 60,  # 5 minutes
            'MAX_ENTRIES': 30,  # limit for clean-up using fifo
            'CULL_FREQUENCY': 3,  # 1/n amount of entries to clean-up
        }
    },
    'public': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'PUBLIC_CACHE_TABLE',
        'OPTIONS': {
            'TIMEOUT': 15 * 60,  # 15 minutes
            'MAX_ENTRIES': 10,  # limit for clean-up using fifo
            'CULL_FREQUENCY': 3,  # 1/n amount of entries to clean-up
        }
    },
    'routes': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'ROUTES_CACHE_TABLE',
        'OPTIONS': {
            'TIMEOUT': 30 * 60,  # 30 minutes
            'MAX_ENTRIES': 30,  # limit for clean-up using fifo
            'CULL_FREQUENCY': 3,  # 1/n amount of entries to clean-up
        }
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

from django.utils.translation import ugettext_lazy as _

# Available languages
LANGUAGES = [
    ('fi', _('Suomi')),
    ('en', _('Englanti')),
    ('sv', _('Ruotsi')),
]

LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'papukaaniApp', 'locale'),
]

# Default language if we can't determine user's preference
LANGUAGE_CODE = 'fi'

TIME_ZONE = 'Europe/Helsinki'

USE_TZ = True

USE_I18N = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

LAJISTORE_URL = 'https://lajistore.laji.fi/'
LAJISTORE_COLLECTIONID = 'http://tun.fi/HR.1427'
TIPUAPI_URL = 'https://fmnh-ws-test.it.helsinki.fi/tipu-api/species'

LAJIAUTH_URL = "https://fmnh-ws-test.it.helsinki.fi/laji-auth/"

LAJIAUTH_USER = os.environ["LAJIAUTH_USER"]

STATIC_ROOT = os.path.join(PROJECT_DIR, '../../static/')

TEST_RUNNER = "papukaani.test_runner.TestRunner"

XEPHYR_VISIBILITY = 0

MOCK_AUTHENTICATION = "Off"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'logfile': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'papukaani.log',
            'maxBytes': 1024 * 100,
            'backupCount': 3,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'logfile'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
        'papukaaniApp': {
            'handlers': ['console', 'logfile'],
            'level': os.getenv('PAPUKAANI_LOG_LEVEL', 'WARN'),
        },
        'papukaaniApp.lajistore_requests_summary': {
            'handlers': ['console', 'logfile'],
            'level': os.getenv('PAPUKAANI_LOG_LEVEL', 'WARN'),
            'propagate': False,
        },
        'papukaaniApp.lajistore_requests': {
            'handlers': ['console', 'logfile'],
            'level': os.getenv('PAPUKAANI_LOG_LEVEL', 'WARN'),
            'propagate': False,
        },
        'papukaaniApp.requests': {
            'handlers': ['logfile'],
            'level': os.getenv('PAPUKAANI_LOG_LEVEL', 'WARN'),
            'propagate': False,
        },
    },
}
