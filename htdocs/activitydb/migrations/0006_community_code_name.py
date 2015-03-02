# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0005_auto_20150227_1601'),
    ]

    operations = [
        migrations.AddField(
            model_name='community',
            name='code_name',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Code Name', blank=True),
            preserve_default=True,
        ),
    ]
