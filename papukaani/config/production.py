from __future__ import absolute_import
from .common import *
import os

SECRET_KEY = os.environ["PAPUKAANI_SECRET_KEY"]

DEBUG = False

ALLOWED_HOSTS += ["*"]

