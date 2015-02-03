# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programdb', '0002_auto_20150202_1342'),
    ]

    operations = [
        migrations.RenameField(
            model_name='program',
            old_name='fundingstatus',
            new_name='funding_status',
        ),
    ]
