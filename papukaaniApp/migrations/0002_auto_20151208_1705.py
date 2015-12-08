# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('papukaaniApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='mappoint',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='mappoint',
            name='creature',
        ),
        migrations.DeleteModel(
            name='Creature',
        ),
        migrations.DeleteModel(
            name='MapPoint',
        ),
    ]
