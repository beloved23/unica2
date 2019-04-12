# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-06-07 21:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0028_auto_20170518_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travel',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
