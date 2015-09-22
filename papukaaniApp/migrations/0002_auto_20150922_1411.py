# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('papukaaniApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mappoint',
            name='altitude',
            field=models.DecimalField(decimal_places=3, max_digits=8),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='latitude',
            field=models.DecimalField(decimal_places=9, max_digits=12),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='longitude',
            field=models.DecimalField(decimal_places=9, max_digits=12),
        ),
        migrations.AlterField(
            model_name='mappoint',
            name='temperature',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
    ]
