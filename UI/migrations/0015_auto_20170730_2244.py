# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-30 16:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UI', '0014_auto_20170730_2220'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobapplicant',
            name='rank',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='deadline',
            field=models.DateField(default=datetime.datetime(2017, 8, 6, 22, 44, 49, 871648)),
        ),
    ]
