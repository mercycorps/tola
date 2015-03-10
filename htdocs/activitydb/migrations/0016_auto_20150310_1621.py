# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0015_auto_20150309_1718'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectproposal',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='meta_instance_id',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='meta_instance_name',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='odk_id',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='odk_index',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='odk_notes',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='odk_parent_table_name',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='odk_submission_time',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='odk_tags',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='odk_uuid',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='profile_code',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='start_time',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='today',
        ),
        migrations.AddField(
            model_name='projectproposal',
            name='community_mobilizer',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Community Mobilizer', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectproposal',
            name='community_rep',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Community Representative', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectproposal',
            name='community_rep_contact',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Community Representative Contact', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectproposal',
            name='sector',
            field=models.ForeignKey(blank=True, to='activitydb.Sector', max_length=255, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='rej_letter',
            field=models.BooleanField(default=False, verbose_name=b'If Rejected: Rejection Letter Sent?'),
            preserve_default=True,
        ),
    ]
