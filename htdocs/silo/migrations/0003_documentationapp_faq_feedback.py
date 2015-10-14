# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silo', '0002_silo_shared'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentationApp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, null=True, blank=True)),
                ('documentation', models.TextField(null=True, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('create_date',),
            },
        ),
        migrations.CreateModel(
            name='FAQ',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.TextField(null=True, blank=True)),
                ('answer', models.TextField(null=True, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('create_date',),
            },
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('note', models.TextField()),
                ('page', models.CharField(max_length=135)),
                ('severity', models.CharField(max_length=135)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('submitter', models.ForeignKey(to='silo.TolaUser')),
            ],
            options={
                'ordering': ('create_date',),
            },
        ),
    ]
