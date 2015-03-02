# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0002_auto_20150224_1327'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='cost_center',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Fund Code', blank=True),
            preserve_default=True,
        ),
    ]
