# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-23 13:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0005_advance_travel'),
    ]

    operations = [
        migrations.AddField(
            model_name='travel',
            name='advance_total',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='travel',
            name='estimated_cost',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
