# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programdb', '0007_auto_20150205_1341'),
    ]

    operations = [
        migrations.CreateModel(
            name='Community',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, verbose_name=b'Community', blank=True)),
                ('latitude', models.CharField(max_length=255, null=True, verbose_name=b'Latitude (Coordinates)', blank=True)),
                ('longitude', models.CharField(max_length=255, null=True, verbose_name=b'Longitude (Coordinates)', blank=True)),
                ('community_rep', models.CharField(max_length=255, null=True, verbose_name=b'Community Representative', blank=True)),
                ('community_rep_contact', models.CharField(max_length=255, null=True, verbose_name=b'Community Representative Contact', blank=True)),
                ('community_mobilizer', models.CharField(max_length=255, null=True, verbose_name=b'Community Mobilizer', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('cluster', models.ForeignKey(blank=True, to='programdb.Cluster', null=True)),
                ('country', models.ForeignKey(to='programdb.Country')),
                ('district', models.ForeignKey(blank=True, to='programdb.District', null=True)),
                ('province', models.ForeignKey(blank=True, to='programdb.Province', null=True)),
                ('village', models.ForeignKey(blank=True, to='programdb.Village', null=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=135, verbose_name=b'Name of Document')),
                ('documentation_type', models.CharField(max_length=135, verbose_name=b'Type (File or URL)')),
                ('description', models.CharField(max_length=255)),
                ('file_field', models.FileField(null=True, upload_to=b'uploads', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='cluster',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='community_mobilizer',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='community_rep',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='community_rep_contact',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='country',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='district',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='province',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='village',
        ),
        migrations.RemoveField(
            model_name='projectcomplete',
            name='cluster',
        ),
        migrations.RemoveField(
            model_name='projectcomplete',
            name='country',
        ),
        migrations.RemoveField(
            model_name='projectcomplete',
            name='district',
        ),
        migrations.RemoveField(
            model_name='projectcomplete',
            name='documentation',
        ),
        migrations.RemoveField(
            model_name='projectcomplete',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='projectcomplete',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='projectcomplete',
            name='province',
        ),
        migrations.RemoveField(
            model_name='projectcomplete',
            name='village',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='cluster',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='community_mobilizer',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='community_rep',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='community_rep_contact',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='country',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='district',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='province',
        ),
        migrations.RemoveField(
            model_name='projectproposal',
            name='village',
        ),
        migrations.AddField(
            model_name='documentation',
            name='project_proposal_id',
            field=models.ForeignKey(blank=True, to='programdb.ProjectProposal', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documentation',
            name='template',
            field=models.ForeignKey(blank=True, to='programdb.Template', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='community',
            field=models.ManyToManyField(to='programdb.Community', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectproposal',
            name='community',
            field=models.ManyToManyField(to='programdb.Community', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documentation',
            name='documentation_type',
            field=models.CharField(max_length=135, verbose_name=b'Type (File or URL)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='project_title',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Project Title', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='project_type',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Project Type', blank=True),
            preserve_default=True,
        ),
    ]
