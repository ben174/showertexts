# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0005_auto_20150916_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='date_renewed',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
