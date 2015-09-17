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
<<<<<<< HEAD
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
=======
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
>>>>>>> 50a08a16168419ca65f66fbc4bb52f71c064d20e
                ('name', models.CharField(max_length=300)),
                ('gpsNumber', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MapPoint',
            fields=[
<<<<<<< HEAD
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('timestamp', models.DateTimeField()),
                ('latitude', models.DecimalField(decimal_places=9, max_digits=12)),
                ('longitude', models.DecimalField(decimal_places=9, max_digits=12)),
                ('altitude', models.DecimalField(decimal_places=3, max_digits=8)),
                ('temperature', models.DecimalField(decimal_places=2, max_digits=5)),
                ('public', models.BooleanField(default=False)),
=======
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('timestamp', models.DateTimeField()),
                ('latitude', models.DecimalField(max_digits=12, decimal_places=9)),
                ('longitude', models.DecimalField(max_digits=12, decimal_places=9)),
                ('altitude', models.DecimalField(max_digits=8, decimal_places=3)),
                ('temperature', models.DecimalField(max_digits=5, decimal_places=2)),
                ('public', models.BooleanField()),
>>>>>>> 50a08a16168419ca65f66fbc4bb52f71c064d20e
                ('creature', models.ForeignKey(to='papukaaniApp.Creature')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='mappoint',
            unique_together=set([('creature', 'timestamp')]),
        ),
    ]
