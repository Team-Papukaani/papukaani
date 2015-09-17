# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('papukaaniApp', '0002_auto_20150917_1247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mappoint',
            name='creature',
            field=models.ForeignKey(primary_key=True, to='papukaaniApp.Creature'),
        ),
    ]
