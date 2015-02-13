# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silo', '__first__'),
        ('programdb', '0010_projectcomplete_approval'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentation',
            name='silo',
            field=models.ForeignKey(blank=True, to='silo.Silo', null=True),
            preserve_default=True,
        ),
    ]
