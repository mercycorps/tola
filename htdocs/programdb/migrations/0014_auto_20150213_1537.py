# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programdb', '0013_auto_20150213_1509'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentation',
            name='documentation_type',
        ),
        migrations.AddField(
            model_name='documentation',
            name='url',
            field=models.CharField(max_length=135, null=True, verbose_name=b'URL (Link to document or document repository)', blank=True),
            preserve_default=True,
        ),
    ]
