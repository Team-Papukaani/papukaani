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
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='GeneralParser',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('formatName', models.CharField(max_length=50)),
                ('gpsNumber', models.CharField(max_length=50, blank=True)),
                ('gpsTime', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('latitude', models.CharField(max_length=50)),
                ('altitude', models.CharField(max_length=50, blank=True)),
                ('temperature', models.CharField(max_length=50, blank=True)),
                ('delimiter', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MapPoint',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('gpsNumber', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField()),
                ('latitude', models.DecimalField(decimal_places=9, max_digits=12)),
                ('longitude', models.DecimalField(decimal_places=9, max_digits=12)),
                ('altitude', models.DecimalField(decimal_places=3, max_digits=8)),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=5)),
                ('public', models.BooleanField(default=False)),
                ('creature', models.ForeignKey(to='papukaaniApp.Creature')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='mappoint',
            unique_together=set([('gpsNumber', 'timestamp', 'latitude', 'longitude')]),
        ),
    ]
