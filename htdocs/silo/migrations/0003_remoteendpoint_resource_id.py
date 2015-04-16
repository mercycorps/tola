# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silo', '0002_auto_20150415_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='remoteendpoint',
            name='resource_id',
            field=models.CharField(max_length=200, null=True, blank=True),
            preserve_default=True,
        ),
    ]
