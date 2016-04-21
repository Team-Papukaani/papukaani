#!/usr/bin/env python
import os
import sys

from papukaani.config import common


if __name__ == "__main__":
    if "test" in sys.argv:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "papukaani.config.test")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "papukaani.config.development")

    if '--visible' in sys.argv:
        common.XEPHYR_VISIBILITY = 1
        sys.argv.remove('--visible')
    else:
        common.XEPHYR_VISIBILITY = 0

    if '--mockauth' in sys.argv:
        common.MOCK_AUTHENTICATION = "On"

    if '--skipauth' in sys.argv:
        common.MOCK_AUTHENTICATION = "Skip"

    from django.core.management import execute_from_command_line

    sysargs = sys.argv.copy()
    if "--mockauth" in sysargs : sysargs.remove('--mockauth')
    if "--skipauth" in sysargs : sysargs.remove('--skipauth')

    execute_from_command_line(sysargs)
