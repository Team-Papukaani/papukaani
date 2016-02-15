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
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('file', models.FileField(upload_to='')),
                ('filename', models.CharField(blank=True, max_length=40)),
                ('uploadTime', models.DateTimeField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='GeneralParser',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('formatName', models.CharField(max_length=50)),
                ('manufacturerID', models.CharField(blank=True, max_length=50)),
                ('timestamp', models.CharField(blank=True, max_length=50)),
                ('time', models.CharField(blank=True, max_length=50)),
                ('date', models.CharField(blank=True, max_length=50)),
                ('longitude', models.CharField(max_length=50)),
                ('latitude', models.CharField(max_length=50)),
                ('altitude', models.CharField(blank=True, max_length=50)),
                ('temperature', models.CharField(blank=True, max_length=50))
            ],
        ),
    ]
