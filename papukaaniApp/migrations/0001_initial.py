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
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='FileStorage',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('filename', models.CharField(blank=True, max_length=40)),
                ('uploadTime', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GeneralParser',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('formatName', models.CharField(max_length=50)),
                ('gpsNumber', models.CharField(blank=True, max_length=50)),
                ('gpsTime', models.CharField(max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('latitude', models.CharField(max_length=50)),
                ('altitude', models.CharField(blank=True, max_length=50)),
                ('temperature', models.CharField(blank=True, max_length=50)),
                ('delimiter', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='MapPoint',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
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
