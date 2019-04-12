# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-22 04:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0047_approvals_approval_person_level'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvals',
            name='status',
            field=models.CharField(choices=[('COMPLETED', 'COMPLETED'), ('PENDING', 'PENDING'), ('EXPIRED', 'EXPIRED')], max_length=10, null=True),
        ),
    ]
