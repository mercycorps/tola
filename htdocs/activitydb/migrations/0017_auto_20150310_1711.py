# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0016_auto_20150310_1621'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectagreement',
            name='contribution',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='quantitative_outputs',
        ),
        migrations.RemoveField(
            model_name='projectcomplete',
            name='actual_contribution',
        ),
        migrations.RemoveField(
            model_name='projectcomplete',
            name='quantitative_outputs',
        ),
        migrations.AddField(
            model_name='contribution',
            name='project_agreement',
            field=models.ForeignKey(related_name='c_agreement', blank=True, to='activitydb.ProjectAgreement', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contribution',
            name='project_complete',
            field=models.ForeignKey(related_name='c_complete', blank=True, to='activitydb.ProjectComplete', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quantitativeoutputs',
            name='project_agreement',
            field=models.ForeignKey(related_name='q_agreement', blank=True, to='activitydb.ProjectAgreement', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quantitativeoutputs',
            name='project_complete',
            field=models.ForeignKey(related_name='q_complete', blank=True, to='activitydb.ProjectAgreement', null=True),
            preserve_default=True,
        ),
    ]
