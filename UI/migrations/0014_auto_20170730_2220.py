# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-30 16:35
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UI', '0013_auto_20170730_1918'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='deadline',
            field=models.DateField(default=datetime.datetime(2017, 8, 6, 22, 20, 14, 774192)),
        ),
        migrations.AlterField(
            model_name='jobapplicant',
            name='certificationScore',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='jobapplicant',
            name='educationScore',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='jobapplicant',
            name='skillScore',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=4),
        ),
        migrations.AlterField(
            model_name='jobapplicant',
            name='workExpScore',
            field=models.DecimalField(decimal_places=1, default=0.0, max_digits=4),
        ),
    ]
