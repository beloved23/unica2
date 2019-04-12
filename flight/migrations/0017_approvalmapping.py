# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-04-08 09:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20170407_1230'),
        ('flight', '0016_travel_reference'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovalMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line_manager', models.CharField(max_length=10, null=True)),
                ('functional_head', models.CharField(max_length=10, null=True)),
                ('cco', models.CharField(max_length=10, null=True)),
                ('hrd', models.CharField(max_length=10, null=True)),
                ('travel_desk', models.CharField(max_length=10, null=True)),
                ('budget_team', models.CharField(max_length=10, null=True)),
                ('payable_account', models.CharField(max_length=10, null=True)),
                ('approval_status', models.CharField(blank=True, choices=[('Approved', 'Approved'), ('Rejected', 'Rejected')], max_length=30, null=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.UserProfile')),
            ],
        ),
    ]
