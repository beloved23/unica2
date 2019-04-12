# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-10 22:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0033_auto_20170610_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='center_code',
            field=models.CharField(blank=True, help_text='Cost Center code to be charged', max_length=20, null=True),
        ),
    ]
