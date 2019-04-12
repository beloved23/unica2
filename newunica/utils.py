from __future__ import unicode_literals
import logging
import os
import urllib, urllib2
import uuid
from django.conf import settings
import re, os

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'travel.log')
#LOG_FILE = "/var/log1/travelportal/approval.log"

logger = logging.getLogger('newunica')
handler = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

ADMIN_CONTEXT = {
    #'opts': RetailerInfo._meta,
    'change': False,
    'is_popup': False,
    'save_as': False,
    #'title': 'Import Retailers',
    'show_delete': False,
    'has_change_permission': True,
    'has_delete_permission': False,
    'has_add_permission': True,
    'add': True,
    #'app_label': 'Retailer',
}


def send_sms(to, msg, short_code='Airtel'):
    '''
    Send message to subscriber using short_code
    '''
    to = '234%s' % to[-10:]
    params = {
            'text': msg,
            'username': settings.SMS_USERNAME,
            'password': settings.SMS_PASSWORD,
            'to': to
            }

    url = settings.SMS_SEND_URL + urllib.urlencode(params)
    print url
    try:
        response = urllib2.urlopen(url)
    except Exception, exc:
        logger.error('url: %s, shortcode: %s, error: %s' % (
            url, short_code, str(exc)))
    else:
        logger.info('msisdn: %s, response: %s' %(to, response.read()))


def normalize(msisdn):
  '''Converts msisdn to 234 format'''
  return '234%s' % msisdn.strip()[-10:]


def clean_data(data):
    patt = re.compile('\+?\d+')
    num_errors = []
    msisdns = []
    off_net = []
    incomplete = []
    for row in data:
        match = patt.match(str(row))
        if match:
            msisdn = normalize(match.group())
            if len(msisdn) not in [10, 13]:
                incomplete.append(msisdn)
                continue
                # if msisdn[:-7] in settings.AIRTEL_PREFIX:
            msisdns.append(msisdn)  # valid airtel number
            # else:
            #     off_net.append(msisdn)  #invalid airtel number
        else:
            # invalid msisdn
            num_errors.append(row)
    return msisdns
