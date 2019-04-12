# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from task import send_campaign
# Create your tests here.



def test():
    send_campaign.delay('Bonus', 'Thanks', 'f77e4ba6-5769-11e9-a604-8c8590b996ed', 1)


test()