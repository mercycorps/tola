# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programdb', '0003_auto_20150202_1346'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectCompletion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('profile_code', models.CharField(max_length=255, verbose_name=b'Profile Code', blank=True)),
                ('proposal_num', models.CharField(max_length=255, verbose_name=b'Proposal Number', blank=True)),
                ('date_of_request', models.DateTimeField(null=True, verbose_name=b'Date of Request', blank=True)),
                ('project_title', models.CharField(max_length=255, verbose_name=b'Project Title', blank=True)),
                ('project_type', models.CharField(max_length=255, verbose_name=b'Proposal Number', blank=True)),
                ('latitude', models.CharField(max_length=255, null=True, verbose_name=b'Latitude (Coordinates)', blank=True)),
                ('longitude', models.CharField(max_length=255, null=True, verbose_name=b'Longitude (Coordinates)', blank=True)),
                ('community_rep', models.CharField(max_length=255, verbose_name=b'Community Representative', blank=True)),
                ('community_rep_contact', models.CharField(max_length=255, verbose_name=b'Community Representative Contact', blank=True)),
                ('community_mobilizer', models.CharField(max_length=255, verbose_name=b'Community Mobilizer', blank=True)),
                ('cluster', models.ForeignKey(blank=True, to='programdb.Cluster', null=True)),
                ('country', models.ForeignKey(to='programdb.Country')),
                ('district', models.ForeignKey(blank=True, to='programdb.District', null=True)),
                ('program', models.ForeignKey(blank=True, to='programdb.Program', null=True)),
                ('project_agreement', models.ForeignKey(to='programdb.ProjectAgreement')),
                ('project_proposal', models.ForeignKey(to='programdb.ProjectProposal')),
                ('province', models.ForeignKey(blank=True, to='programdb.Province', null=True)),
                ('village', models.ForeignKey(blank=True, to='programdb.Village', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mergemap',
            name='project_agreement',
            field=models.ForeignKey(to='programdb.ProjectAgreement', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mergemap',
            name='project_completion',
            field=models.ForeignKey(to='programdb.ProjectCompletion', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='latitude',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Latitude (Coordinates)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='longitude',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Longitude (Coordinates)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='mergemap',
            name='project_proposal',
            field=models.ForeignKey(to='programdb.ProjectProposal', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='programdashboard',
            name='project_agreement',
            field=models.ForeignKey(to='programdb.ProjectAgreement', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='programdashboard',
            name='project_completion',
            field=models.ForeignKey(to='programdb.ProjectCompletion', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='programdashboard',
            name='project_proposal',
            field=models.ForeignKey(to='programdb.ProjectProposal', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='latitude',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Latitude (Coordinates)', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='longitude',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Longitude (Coordinates)', blank=True),
            preserve_default=True,
        ),
    ]
