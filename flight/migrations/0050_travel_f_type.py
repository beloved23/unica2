# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-11-29 02:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0049_auto_20170927_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='f_type',
            field=models.BooleanField(default=False),
        ),
    ]
