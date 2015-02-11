# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('programdb', '0008_auto_20150209_0915'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectagreement',
            name='approval',
            field=models.BooleanField(default=None, verbose_name=b'Approval'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectagreement',
            name='program',
            field=models.ForeignKey(related_name='agreement', blank=True, to='programdb.Program', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectcomplete',
            name='program',
            field=models.ForeignKey(related_name='complete', blank=True, to='programdb.Program', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='projectproposal',
            name='program',
            field=models.ForeignKey(related_name='proposal', blank=True, to='programdb.Program', null=True),
            preserve_default=True,
        ),
    ]
