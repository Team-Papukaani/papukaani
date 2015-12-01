# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('papukaaniApp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filestorage',
            old_name='name',
            new_name='filename',
        ),
    ]
