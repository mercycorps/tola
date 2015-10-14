# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('silo', '0004_auto_20151014_1233'),
    ]

    operations = [
        migrations.AlterField(
            model_name='silo',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
