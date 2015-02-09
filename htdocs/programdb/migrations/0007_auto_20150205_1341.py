# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programdb', '0006_auto_20150203_1642'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectagreement',
            options={'ordering': ('create_date',)},
        ),
        migrations.AlterModelOptions(
            name='projectcomplete',
            options={'ordering': ('create_date',)},
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='create_date',
            field=models.DateTimeField(null=True, verbose_name=b'Date Created', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='edit_date',
            field=models.DateTimeField(null=True, verbose_name=b'Last Edit Date', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='create_date',
            field=models.DateTimeField(null=True, verbose_name=b'Date Created', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='edit_date',
            field=models.DateTimeField(null=True, verbose_name=b'Last Edit Date', blank=True),
            preserve_default=True,
        ),
    ]
