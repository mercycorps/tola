# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0011_auto_20150305_1515'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectagreement',
            name='rej_letter',
        ),
    ]
