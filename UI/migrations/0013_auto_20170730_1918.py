# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-30 13:33
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UI', '0012_auto_20170730_0609'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='certification_link',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='deadline',
            field=models.DateField(default=datetime.datetime(2017, 8, 6, 19, 17, 58, 900081)),
        ),
    ]