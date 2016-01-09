# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShowerThought',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('post_id', models.CharField(max_length=20)),
                ('thought_text', models.CharField(max_length=500)),
                ('url', models.URLField(max_length=100)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sms_number', models.CharField(unique=True, max_length=20)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='TextSend',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_sent', models.DateTimeField(auto_now_add=True)),
                ('post_id', models.CharField(max_length=20)),
                ('message_text', models.CharField(max_length=500)),
                ('subscriber', models.ForeignKey(to='texts.Subscriber')),
            ],
        ),
    ]
