# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-03-23 00:00
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0004_travel_objective'),
    ]

    operations = [
        migrations.AddField(
            model_name='advance',
            name='travel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='flight.Travel'),
            preserve_default=False,
        ),
    ]
