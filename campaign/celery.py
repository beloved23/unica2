from __future__ import absolute_import
import os
from celery import Celery
import django
from django.conf import settings


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'newunica.settings')
app = Celery('campaign', bankend='amqp', broker='amqp://cwc:london@172.24.6.103:5672/')
#app = Celery('campaign', bankend='amqp', broker='amqp://cwc:london@localhost:15672/')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request))
