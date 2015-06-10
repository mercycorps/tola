# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datafield',
            name='silo',
        ),
        migrations.RemoveField(
            model_name='valuestore',
            name='field',
        ),
        migrations.DeleteModel(
            name='DataField',
        ),
        migrations.DeleteModel(
            name='ValueStore',
        ),
    ]
