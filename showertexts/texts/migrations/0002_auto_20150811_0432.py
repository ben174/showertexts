# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='textsend',
            name='result_message',
            field=models.CharField(max_length=500, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='textsend',
            name='sucess',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='showerthought',
            name='url',
            field=models.URLField(max_length=300, null=True, blank=True),
        ),
    ]
