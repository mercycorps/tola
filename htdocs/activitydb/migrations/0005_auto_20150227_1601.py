# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0004_auto_20150227_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectagreement',
            name='approval_remarks',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Approval Remarks', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='approval_remarks',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Approval Remarks', blank=True),
            preserve_default=True,
        ),
    ]
