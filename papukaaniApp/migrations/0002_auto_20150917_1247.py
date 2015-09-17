# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('papukaaniApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mappoint',
            name='id',
        ),
        migrations.AddField(
            model_name='mappoint',
            name='public',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='creature',
            field=models.ForeignKey(primary_key=True, to='papukaaniApp.Creature', serialize=False),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='timestamp',
            field=models.DateTimeField(primary_key=True),
        ),
    ]
