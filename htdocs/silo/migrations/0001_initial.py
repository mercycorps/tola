# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import oauth2client.django_orm


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
            name='GoogleCredentialsModel',
            fields=[
                ('id', models.ForeignKey(related_name='google_credentials', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('credential', oauth2client.django_orm.CredentialsField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
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
        migrations.CreateModel(
            name='RemoteEndPoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('link', models.URLField()),
                ('resource_id', models.CharField(max_length=200, null=True, blank=True)),
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
                ('source', models.ForeignKey(to='silo.Read')),
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
                ('char_store', models.CharField(max_length=3000, null=True, blank=True)),
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
            model_name='read',
            name='type',
            field=models.ForeignKey(to='silo.ReadType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datafield',
            name='silo',
            field=models.ForeignKey(to='silo.Silo'),
            preserve_default=True,
        ),
    ]
