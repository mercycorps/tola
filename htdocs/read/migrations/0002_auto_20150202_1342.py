# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('read', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Read',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('read_name', models.CharField(default=b'', max_length=100, verbose_name=b'source name', blank=True)),
                ('read_url', models.CharField(default=b'', max_length=100, verbose_name=b'source url', blank=True)),
                ('description', models.TextField()),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('file_data', models.FileField(upload_to=b'uploads', null=True, verbose_name=b'Upload CSV File', blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('create_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ReadType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('read_type', models.CharField(max_length=135, blank=True)),
                ('description', models.CharField(max_length=765, blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='read',
            name='type',
            field=models.ForeignKey(to='read.ReadType'),
            preserve_default=True,
        ),
    ]
