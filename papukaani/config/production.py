from __future__ import absolute_import
from .common import *
import os

SECRET_KEY = os.environ["PAPUKAANI_SECRET_KEY"]

DEBUG = False

ALLOWED_HOSTS += ["papukaani-test.luomus.fi", "fmnh-ws-test.it.helsinki.fi"]

STATIC_ROOT = os.path.join(PROJECT_DIR, '../../static/')
