# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-08 17:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0030_travel_ticket_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='ticket_no',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
