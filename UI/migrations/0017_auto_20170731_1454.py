# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-31 09:09
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('UI', '0016_auto_20170731_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicant',
            name='photo',
            field=models.ImageField(default='static/user_photos/anupam.jpg', upload_to='static/user_photos'),
        ),
        migrations.AlterField(
            model_name='job',
            name='deadline',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 7, 9, 9, 1, 459273, tzinfo=utc)),
        ),
    ]