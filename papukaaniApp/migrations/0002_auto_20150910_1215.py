# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('papukaaniApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Creature',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('gpsNumber', models.IntegerField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='MapPoint',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('latitude', models.DecimalField(decimal_places=9, max_digits=12)),
                ('longitude', models.DecimalField(decimal_places=9, max_digits=12)),
                ('altitude', models.DecimalField(decimal_places=3, max_digits=8)),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.DeleteModel(
            name='Test',
        ),
    ]
