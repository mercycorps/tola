# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0009_auto_20150303_1101'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectagreement',
            name='benchmarks',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='monitor',
        ),
        migrations.AddField(
            model_name='benchmarks',
            name='agreement',
            field=models.ForeignKey(blank=True, to='activitydb.ProjectAgreement', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='benchmarks',
            name='complete',
            field=models.ForeignKey(blank=True, to='activitydb.ProjectComplete', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitor',
            name='agreement',
            field=models.ForeignKey(blank=True, to='activitydb.ProjectAgreement', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='monitor',
            name='complete',
            field=models.ForeignKey(blank=True, to='activitydb.ProjectComplete', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='contribution',
            field=models.ForeignKey(related_name='contribute_agree', blank=True, to='activitydb.Contribution', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='capacity',
            field=models.ForeignKey(related_name='quant_out_agree', blank=True, to='activitydb.Capacity', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='evaluate',
            field=models.ForeignKey(related_name='quant_out_agree', blank=True, to='activitydb.Evaluate', null=True),
            preserve_default=True,
        ),
    ]
