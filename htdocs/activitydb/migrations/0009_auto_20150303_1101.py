# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0008_auto_20150303_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='benchmarks',
            name='percent_complete',
            field=models.IntegerField(max_length=25, null=True, verbose_name=b'% complete', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='benchmarks',
            name='percent_cumulative',
            field=models.IntegerField(max_length=25, null=True, verbose_name=b'% cumulative completion', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='capacity',
            name='capacity',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Capacity', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='evaluate',
            name='evaluate',
            field=models.CharField(max_length=255, null=True, verbose_name=b'How will you evaluate the outcome or impact of the project?', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='monitor',
            name='frequency',
            field=models.IntegerField(max_length=25, null=True, verbose_name=b'Frequency', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='monitor',
            name='responsible_person',
            field=models.CharField(max_length=25, null=True, verbose_name=b'Person Responsible', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='partners',
            field=models.BooleanField(default=0, verbose_name=b'Are there partners involved?'),
            preserve_default=True,
        ),
    ]
