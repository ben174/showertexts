# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0006_auto_20150917_0906'),
    ]

    operations = [
        migrations.AddField(
            model_name='showerthought',
            name='bot_notified',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subscriber',
            name='note',
            field=models.CharField(max_length=100, null=True, blank=True),
        ),
    ]
