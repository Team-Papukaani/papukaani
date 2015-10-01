# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('papukaaniApp', '0002_auto_20150922_1411'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mappoint',
            unique_together=set([('gpsNumber', 'timestamp', 'latitude', 'longitude')]),
        ),
    ]
