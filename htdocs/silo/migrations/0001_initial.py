# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.auth.models
import oauth2client.django_orm
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='GoogleCredentialsModel',
            fields=[
                ('id', models.ForeignKey(related_name='google_credentials', primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('credential', oauth2client.django_orm.CredentialsField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Read',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('read_name', models.CharField(default=b'', max_length=100, verbose_name=b'source name', blank=True)),
                ('description', models.TextField()),
                ('read_url', models.CharField(default=b'', max_length=100, verbose_name=b'source url', blank=True)),
                ('resource_id', models.CharField(max_length=200, null=True, blank=True)),
                ('username', models.CharField(max_length=20, null=True, blank=True)),
                ('token', models.CharField(max_length=254, null=True, blank=True)),
                ('file_data', models.FileField(upload_to=b'uploads', null=True, verbose_name=b'Upload CSV File', blank=True)),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('edit_date', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
                'ordering': ('create_date',),
            },
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
        ),
        migrations.CreateModel(
            name='Silo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('description', models.CharField(max_length=255, null=True, blank=True)),
                ('public', models.BooleanField()),
                ('create_date', models.DateTimeField(null=True, blank=True)),
            ],
            options={
                'ordering': ('create_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ThirdPartyTokens',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=60)),
                ('token', models.CharField(max_length=255)),
                ('create_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('edit_date', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TolaUser',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='thirdpartytokens',
            name='user',
            field=models.ForeignKey(related_name='tokens', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='tag',
            name='owner',
            field=models.ForeignKey(related_name='tags', to='silo.TolaUser'),
        ),
        migrations.AddField(
            model_name='silo',
            name='owner',
            field=models.ForeignKey(to='silo.TolaUser'),
        ),
        migrations.AddField(
            model_name='silo',
            name='reads',
            field=models.ManyToManyField(related_name='silos', to='silo.Read'),
        ),
        migrations.AddField(
            model_name='silo',
            name='tags',
            field=models.ManyToManyField(related_name='silos', to='silo.Tag', blank=True),
        ),
        migrations.AddField(
            model_name='read',
            name='owner',
            field=models.ForeignKey(to='silo.TolaUser'),
        ),
        migrations.AddField(
            model_name='read',
            name='type',
            field=models.ForeignKey(to='silo.ReadType'),
        ),
    ]
