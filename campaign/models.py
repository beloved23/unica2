# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.
from account.models import *
from django.db import models
# Create your models here.

CONTENT_TYPE = (
                ('Text', 'Text'),
                ('Flash', 'Flash'),
                )

STATUS = (
                ('Pending', 'Pending'),
                ('Running', 'Running'),
                ('Completed', 'Completed')
                )


class Sender(models.Model):
    name = models.CharField(max_length=10, null=False, blank=False)


class Uploads(models.Model):
    user = models.ForeignKey(User, related_name="user_profile_upload")
    name = models.CharField(max_length=100, null=False, blank=False)
    name_id = models.CharField(max_length=50, null=False, blank=False)
    recipient_count = models.CharField(max_length=150, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name


class Broadcast(models.Model):
    user = models.ForeignKey(User, related_name="user_profile_broad")
    broadcast_name = models.CharField(max_length=30, null=False, blank=False, help_text="Campaign Name")
    broadcast_description = models.CharField(max_length=150, null=True, blank=True, help_text="Campaign Description")
    content_type = models.CharField(max_length=12, null=False, blank=False, choices=CONTENT_TYPE)
    sender = models.CharField(max_length=30, null=False, blank=False, help_text="Sender")
    message = models.TextField()
    base_file = models.ForeignKey(Uploads, null=True, blank=True)
    schedule_start = models.DateTimeField(null=True,blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    sms_upload_path = models.CharField(max_length=150, null=True, blank=True, help_text="Please upload file")
    recipient_count = models.CharField(max_length=150, null=True, blank=True)
    status = models.CharField(max_length=15, null=False, blank=False, choices=STATUS)
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.broadcast_name


class Push(models.Model):
    content_type = models.CharField(max_length=12, null=False, blank=False, choices=CONTENT_TYPE)
    message = models.TextField()
    schedule_start = models.DateTimeField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.broadcast_name











