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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('gpsNumber', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='MapPoint',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
            unique_together=set([('creature', 'timestamp')]),
        ),
    ]
