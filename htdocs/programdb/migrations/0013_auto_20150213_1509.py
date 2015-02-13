# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programdb', '0012_projectcomplete_project_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='documentation',
            old_name='project_proposal_id',
            new_name='project',
        ),
    ]
