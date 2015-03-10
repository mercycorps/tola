# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0014_auto_20150309_1607'),
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficiary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('beneficiary_name', models.CharField(max_length=255, null=True, blank=True)),
                ('father_name', models.CharField(max_length=255, null=True, blank=True)),
                ('age', models.IntegerField(null=True, blank=True)),
                ('gender', models.CharField(max_length=255, null=True, blank=True)),
                ('community', models.CharField(max_length=255, null=True, blank=True)),
                ('signature', models.CharField(max_length=255, null=True, blank=True)),
                ('remarks', models.CharField(max_length=255, null=True, blank=True)),
                ('initials', models.CharField(max_length=255, null=True, blank=True)),
                ('contact_num', models.CharField(max_length=255, null=True, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('beneficiary_name',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TrainingAttendance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('training_name', models.CharField(max_length=255)),
                ('implementer', models.CharField(max_length=255, null=True, blank=True)),
                ('reporting_period', models.CharField(max_length=255, null=True, blank=True)),
                ('total_participants', models.IntegerField(null=True, blank=True)),
                ('location', models.CharField(max_length=255, null=True, blank=True)),
                ('community', models.CharField(max_length=255, null=True, blank=True)),
                ('training_duration', models.CharField(max_length=255, null=True, blank=True)),
                ('start_date', models.CharField(max_length=255, null=True, blank=True)),
                ('end_date', models.CharField(max_length=255, null=True, blank=True)),
                ('trainer_name', models.CharField(max_length=255, null=True, blank=True)),
                ('trainer_contact_num', models.CharField(max_length=255, null=True, blank=True)),
                ('total_male', models.IntegerField(null=True, blank=True)),
                ('total_female', models.IntegerField(null=True, blank=True)),
                ('total_age_0_14_male', models.IntegerField(null=True, blank=True)),
                ('total_age_0_14_female', models.IntegerField(null=True, blank=True)),
                ('total_age_15_24_male', models.IntegerField(null=True, blank=True)),
                ('total_age_15_24_female', models.IntegerField(null=True, blank=True)),
                ('total_age_25_59_male', models.IntegerField(null=True, blank=True)),
                ('total_age_25_59_female', models.IntegerField(null=True, blank=True)),
                ('total_age_60_male', models.IntegerField(null=True, blank=True)),
                ('total_age_60_female', models.IntegerField(null=True, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('program', models.ForeignKey(blank=True, to='activitydb.Program', null=True)),
                ('project_proposal', models.ForeignKey(blank=True, to='activitydb.ProjectProposal', null=True)),
            ],
            options={
                'ordering': ('training_name',),
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='training',
            field=models.ForeignKey(blank=True, to='activitydb.TrainingAttendance', null=True),
            preserve_default=True,
        ),
    ]
