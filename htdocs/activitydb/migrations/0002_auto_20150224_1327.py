# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name=b'Office Name', blank=True)),
                ('code', models.CharField(max_length=255, verbose_name=b'Office Code', blank=True)),
                ('create_date', models.DateTimeField(null=True, blank=True)),
                ('edit_date', models.DateTimeField(null=True, blank=True)),
                ('province', models.ForeignKey(to='activitydb.Province')),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='cluster',
            name='district',
        ),
        migrations.RemoveField(
            model_name='community',
            name='cluster',
        ),
        migrations.DeleteModel(
            name='Cluster',
        ),
        migrations.RemoveField(
            model_name='quantitativeoutputs',
            name='in_logframe',
        ),
        migrations.AddField(
            model_name='community',
            name='office',
            field=models.ForeignKey(blank=True, to='activitydb.Office', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='quantitativeoutputs',
            name='logframe_indicator',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Logframe Indicator', blank=True),
            preserve_default=True,
        ),
    ]
