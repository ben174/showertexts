# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texts', '0004_remove_subscriber_expired'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriber',
            name='date_renewed',
            field=models.DateTimeField(),
        ),
    ]
