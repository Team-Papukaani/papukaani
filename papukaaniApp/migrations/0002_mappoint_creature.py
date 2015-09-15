# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('papukaaniApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mappoint',
            name='creature',
            field=models.ForeignKey(to='papukaaniApp.Creature', default=1),
            preserve_default=False,
        ),
    ]
