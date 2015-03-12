# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0012_remove_projectagreement_rej_letter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectagreement',
            name='project_name',
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='project_name',
            field=models.CharField(max_length=255, null=True, verbose_name=b'Project Title', blank=True),
            preserve_default=True,
        ),
    ]
