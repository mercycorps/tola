# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0007_auto_20150302_1410'),
    ]

    operations = [
        migrations.CreateModel(
            name='Benchmarks',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('percent_complete', models.IntegerField(max_length=25, verbose_name=b'% complete', blank=True)),
                ('percent_cumulative', models.IntegerField(max_length=25, verbose_name=b'% cumulative completion', blank=True)),
                ('description', models.CharField(max_length=255, verbose_name=b'Description', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('description',),
                'verbose_name_plural': 'Benchmarks',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Capacity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('capacity', models.CharField(max_length=255, verbose_name=b'Capacity', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('capacity',),
                'verbose_name_plural': 'Capacity',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Evaluate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('evaluate', models.CharField(max_length=255, verbose_name=b'How will you evaluate the outcome or impact of the project?', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('evaluate',),
                'verbose_name_plural': 'Evaluate',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('responsible_person', models.CharField(max_length=25, verbose_name=b'Person Responsible', blank=True)),
                ('frequency', models.IntegerField(max_length=25, verbose_name=b'Frequency', blank=True)),
                ('type', models.TextField(null=True, verbose_name=b'Type', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('type',),
                'verbose_name_plural': 'Monitors',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='other_budget',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='profile_code',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='project_title',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='prop_status',
        ),
        migrations.RemoveField(
            model_name='projectagreement',
            name='sub_code',
        ),
        migrations.RemoveField(
            model_name='quantitativeoutputs',
            name='number_achieved',
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='benchmarks',
            field=models.ForeignKey(related_name='benchmarks_agree', blank=True, to='activitydb.Benchmarks', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='capacity',
            field=models.ForeignKey(related_name='capacity_agree', blank=True, to='activitydb.Capacity', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='evaluate',
            field=models.ForeignKey(related_name='valuate_agree', blank=True, to='activitydb.Evaluate', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='expected_duration',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Expected duration', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='lin_code',
            field=models.CharField(max_length=255, null=True, verbose_name=b'LIN Sub Code', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='monitor',
            field=models.ForeignKey(related_name='monitor_agree', blank=True, to='activitydb.Monitor', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='project_code',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Project Code Number', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='project_design',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Project design for', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='project_name',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Project Name', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='project_status',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Project Status', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='quantitative_outputs',
            field=models.ForeignKey(related_name='quant_out_agree', blank=True, to='activitydb.QuantitativeOutputs', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quantitativeoutputs',
            name='targeted',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Targeted #', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='expected_end_date',
            field=models.DateTimeField(null=True, verbose_name=b'Expected ending date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='expected_start_date',
            field=models.DateTimeField(null=True, verbose_name=b'Expected starting date', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='partners',
            field=models.BooleanField(default=True, verbose_name=b'Are there partners involved?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='rej_letter',
            field=models.TextField(default=False, verbose_name=b'Rejection Letter'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='project_title',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Proposed Project Title', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='rej_letter',
            field=models.BooleanField(default=False, verbose_name=b'Rejection Letter Sent'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='quantitativeoutputs',
            name='description',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Description of Contribution', blank=True),
            preserve_default=True,
        ),
    ]
