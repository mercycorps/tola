# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('activitydb', '0003_program_cost_center'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='community',
            options={'ordering': ('name',), 'verbose_name_plural': 'Communities'},
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ('country',), 'verbose_name_plural': 'Countries'},
        ),
        migrations.AlterModelOptions(
            name='documentation',
            options={'ordering': ('name',), 'verbose_name_plural': 'Documentation'},
        ),
        migrations.AlterModelOptions(
            name='projectagreement',
            options={'ordering': ('create_date',), 'permissions': (('can_approve', 'Can approve proposal'),)},
        ),
        migrations.AlterModelOptions(
            name='projectcomplete',
            options={'ordering': ('create_date',), 'verbose_name_plural': 'Project Completions'},
        ),
        migrations.AlterModelOptions(
            name='projectproposal',
            options={'ordering': ('create_date',), 'permissions': (('can_approve', 'Can approve proposal'),)},
        ),
        migrations.AlterModelOptions(
            name='quantitativeoutputs',
            options={'ordering': ('description',), 'verbose_name_plural': 'Quantitative Outputs'},
        ),
        migrations.AddField(
            model_name='projectagreement',
            name='approval_submitted_by',
            field=models.ForeignKey(related_name='submitted_by_agreement', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='projectcomplete',
            name='approval_submitted_by',
            field=models.ForeignKey(related_name='submitted_by_complete', blank=True, to=settings.AUTH_USER_MODEL, null=True),
            preserve_default=True,
        ),
    ]
