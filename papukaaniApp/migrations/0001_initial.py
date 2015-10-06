# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Creature',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='MapPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('gpsNumber', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField()),
                ('latitude', models.DecimalField(max_digits=12, decimal_places=9)),
                ('longitude', models.DecimalField(max_digits=12, decimal_places=9)),
                ('altitude', models.DecimalField(max_digits=8, decimal_places=3)),
                ('temperature', models.DecimalField(max_digits=5, decimal_places=2)),
                ('public', models.BooleanField(default=False)),
                ('creature', models.ForeignKey(to='papukaaniApp.Creature')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='mappoint',
            unique_together=set([('gpsNumber', 'timestamp', 'latitude', 'longitude')]),
        ),
    ]
