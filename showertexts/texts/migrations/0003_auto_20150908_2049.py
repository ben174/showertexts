# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0002_auto_20150811_0432'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriber',
            name='date_renewed',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 9, 3, 49, 37, 469623, tzinfo=utc), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscriber',
            name='expired',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='subscriber',
            name='lifetime',
            field=models.BooleanField(default=False),
        ),
    ]
