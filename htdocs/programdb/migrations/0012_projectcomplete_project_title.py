# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programdb', '0011_documentation_silo'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectcomplete',
            name='project_title',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Project Title', blank=True),
            preserve_default=True,
        ),
    ]
