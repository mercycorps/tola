# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='silo',
            name='shared',
            field=models.ManyToManyField(related_name='silos', to='silo.TolaUser', blank=True),
        ),
    ]
