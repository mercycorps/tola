# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activitydb', '0018_auto_20150311_1553'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectproposal',
            name='prop_status',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='proposal_review',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='proposal_review_2',
        ),
        migrations.AddField(
            model_name='projectproposal',
            name='community_mobilizer_contact',
            field=models.CharField(max_length=255, null=True, verbose_name=b'MC Community Mobilizer Contact Number', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectproposal',
            name='estimated_by',
            field=models.ForeignKey(related_name='estimate', blank=True, to=settings.AUTH_USER_MODEL, help_text=b'This is the originator', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='approved_by',
            field=models.ForeignKey(related_name='approving', blank=True, to=settings.AUTH_USER_MODEL, help_text=b'This is the Provincial Line Manager', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='community_mobilizer',
            field=models.CharField(max_length=255, null=True, verbose_name=b'MC Community Mobilizer', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='community_rep_contact',
            field=models.CharField(help_text=b'Can have mulitple contact numbers', max_length=255, null=True, verbose_name=b'Community Representative Contact', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='has_rej_letter',
            field=models.BooleanField(default=False, help_text=b'If yes attach copy', verbose_name=b'If Rejected: Rejection Letter Sent?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='project_activity',
            field=models.CharField(help_text=b'This should come directly from the activites listed in the Logframe', max_length=255, null=True, verbose_name=b'Project Activity', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='project_description',
            field=models.TextField(help_text=b'Description must meet the Criteria.  Will translate description into three languages: English, Dari and Pashto)', null=True, verbose_name=b'Project Description', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='project_name',
            field=models.CharField(help_text=b'Please be specific in your name.  Consider that your Project Name includes WHO, WHAT, WHERE, HOW', max_length=255, verbose_name=b'Project Name'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='project_type',
            field=models.ForeignKey(blank=True, to='activitydb.ProjectType', max_length=255, help_text=b'Please refer to Form 05 - Project Progress Summary', null=True),
            preserve_default=True,
        ),
    ]
