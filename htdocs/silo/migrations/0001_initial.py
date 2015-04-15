# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('read', '0002_auto_20150202_1342'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataField',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original_name', models.CharField(max_length=765, blank=True)),
                ('name', models.CharField(max_length=765, blank=True)),
                ('is_uid', models.NullBooleanField()),
                ('published', models.BooleanField(default=b'0')),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RemoteEndPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('link', models.URLField()),
                ('token', models.CharField(max_length=254, null=True, blank=True)),
                ('username', models.CharField(max_length=20, null=True, blank=True)),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('edit_date', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Silo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField()),
                ('description', models.TextField()),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('owner', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('source', models.ForeignKey(to='read.Read')),
            ],
            options={
                'ordering': ('create_date',),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ValueStore',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('char_store', models.CharField(max_length=1000, null=True, blank=True)),
                ('text_store', models.TextField(null=True, blank=True)),
                ('row_number', models.IntegerField(max_length=10, null=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('field', models.ForeignKey(to='silo.DataField')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='remoteendpoint',
            name='silo',
            field=models.ForeignKey(related_name='remote_end_points', to='silo.Silo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datafield',
            name='silo',
            field=models.ForeignKey(to='silo.Silo'),
            preserve_default=True,
        ),
    ]
