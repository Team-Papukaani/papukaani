#!/usr/bin/env python
import os
import sys
from papukaani.config import common as settings

if __name__ == "__main__":

    if "test" in sys.argv:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "papukaani.config.test")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "papukaani.config.development")

    if '--visible' in sys.argv:
        settings.XEPHYR_VISIBILITY = 1
        sys.argv.remove('--visible')
    else:
        settings.XEPHYR_VISIBILITY = 0

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
