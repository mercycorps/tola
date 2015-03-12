# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0017_auto_20150310_1711'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectproposal',
            old_name='rej_letter',
            new_name='has_rej_letter',
        ),
        migrations.RemoveField(
            model_name='beneficiary',
            name='contact_num',
        ),
        migrations.RemoveField(
            model_name='beneficiary',
            name='initials',
        ),
        migrations.RemoveField(
            model_name='community',
            name='office',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='office_code',
        ),
        migrations.RemoveField(
            model_name='trainingattendance',
            name='create_date',
        ),
        migrations.RemoveField(
            model_name='trainingattendance',
            name='edit_date',
        ),
        migrations.RemoveField(
            model_name='trainingattendance',
            name='total_age_60_female',
        ),
        migrations.RemoveField(
            model_name='trainingattendance',
            name='total_age_60_male',
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='office',
            field=models.ForeignKey(blank=True, to='activitydb.Office', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='office',
            field=models.ForeignKey(blank=True, to='activitydb.Office', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='project_activity',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Project Activity', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectproposal',
            name='office',
            field=models.ForeignKey(blank=True, to='activitydb.Office', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectproposal',
            name='project_activity',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Project Activity', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectproposal',
            name='rejection_letter',
            field=models.FileField(upload_to=b'uploads', null=True, verbose_name=b'Proposal Review', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='trainingattendance',
            name='form_filled_by',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='trainingattendance',
            name='form_filled_by_contact_num',
            field=models.CharField(max_length=255, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='community',
            field=models.ForeignKey(blank=True, to='activitydb.Community', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='beneficiary',
            name='signature',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='activity_code',
            field=models.CharField(help_text=b'If applicable at this stage, please request Activity Code from Kabul MEL', max_length=255, null=True, verbose_name=b'Activity Code', blank=True),
            preserve_default=True,
        ),
    ]
