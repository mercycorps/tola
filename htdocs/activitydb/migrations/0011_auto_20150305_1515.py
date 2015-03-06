# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0010_auto_20150304_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='quantitativeoutputs',
            name='non_logframe_indicator',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Logframe Indicator', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='approval',
            field=models.CharField(default=b'in progress', max_length=255, null=True, verbose_name=b'Approval', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='approval',
            field=models.CharField(default=b'in progress', max_length=255, null=True, verbose_name=b'Approval', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='approval',
            field=models.CharField(default=b'in progress', max_length=255, null=True, verbose_name=b'Approval', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quantitativeoutputs',
            name='logframe_indicator',
            field=models.ForeignKey(blank=True, to='indicators.Indicator', null=True),
            preserve_default=True,
        ),
    ]
