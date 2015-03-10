# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0013_auto_20150305_1705'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=135, verbose_name=b'Type of Project')),
                ('description', models.CharField(max_length=255)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='project_title',
            field=models.CharField(max_length=255, verbose_name=b'Proposed Project Title'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='project_type',
            field=models.ForeignKey(blank=True, to='activitydb.ProjectType', max_length=255, null=True),
            preserve_default=True,
        ),
    ]
