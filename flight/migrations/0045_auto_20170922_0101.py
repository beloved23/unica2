# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-22 01:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flight', '0044_approvals_reference'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='approvals',
            options={'verbose_name': 'Approval'},
        ),
        migrations.AlterField(
            model_name='approvals',
            name='approval_person_email',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
