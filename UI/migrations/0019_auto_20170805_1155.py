# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-05 06:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('UI', '0018_auto_20170801_1953'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 12, 6, 10, 14, 351596, tzinfo=utc)),
        ),
    ]
