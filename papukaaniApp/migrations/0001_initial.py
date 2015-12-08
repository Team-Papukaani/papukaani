# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileStorage',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('file', models.FileField(upload_to='')),
                ('filename', models.CharField(max_length=40, blank=True)),
                ('uploadTime', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GeneralParser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
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
    ]
