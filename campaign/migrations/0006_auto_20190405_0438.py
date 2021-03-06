# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-04-05 04:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campaign', '0005_uploads_recipient_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='broadcast',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Running', 'Running'), ('Completed', 'Completed')], default=1, max_length=15),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='broadcast',
            name='content_type',
            field=models.CharField(choices=[('Text', 'Text'), ('Flash', 'Flash')], max_length=12),
        ),
        migrations.AlterField(
            model_name='push',
            name='content_type',
            field=models.CharField(choices=[('Text', 'Text'), ('Flash', 'Flash')], max_length=12),
        ),
    ]
