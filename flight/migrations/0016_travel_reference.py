# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-07 12:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0015_auto_20170406_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='reference',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
