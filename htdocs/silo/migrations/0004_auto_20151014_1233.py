# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('silo', '0003_documentationapp_faq_feedback'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TolaUser',
        ),
        migrations.AlterField(
            model_name='feedback',
            name='submitter',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='read',
            name='owner',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='silo',
            name='owner',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='tag',
            name='owner',
            field=models.ForeignKey(related_name='tags', to=settings.AUTH_USER_MODEL),
        ),
    ]
