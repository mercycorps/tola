# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activitydb', '0006_community_code_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='community',
            old_name='code_name',
            new_name='code',
        ),
    ]
