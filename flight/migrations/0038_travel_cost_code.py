# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-13 16:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0037_auto_20170612_0911'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='cost_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
