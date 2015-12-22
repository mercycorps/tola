# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('silo', '0005_auto_20151014_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='read',
            name='autopull',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='read',
            name='autopull_frequency',
            field=models.CharField(max_length=25, null=True, blank=True, choices=[(b'daily', b'Daily'), (b'weekly', b'Weekly')]),
        ),
    ]
