# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-07-04 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0039_traveladvice'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='is_advice',
            field=models.BooleanField(default=False),
        ),
    ]
