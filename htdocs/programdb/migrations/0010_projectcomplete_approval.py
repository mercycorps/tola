# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programdb', '0009_auto_20150210_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectcomplete',
            name='approval',
            field=models.BooleanField(default=None, verbose_name=b'Approval'),
            preserve_default=True,
        ),
    ]
