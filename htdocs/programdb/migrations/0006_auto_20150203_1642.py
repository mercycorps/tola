# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programdb', '0005_auto_20150203_1156'),
    ]

    operations = [
        migrations.RenameField(
            model_name='projectcomplete',
            old_name='qualitative_outputs',
            new_name='quantitative_outputs',
        ),
        migrations.AlterField(
            model_name='documentation',
            name='file_field',
            field=models.FileField(null=True, upload_to=b'uploads', blank=True),
            preserve_default=True,
        ),
    ]
