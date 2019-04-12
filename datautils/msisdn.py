'''
Created on Sep 25, 2012

@author: anthony
'''
import re
from django.forms import ValidationError
from django.conf import settings

def normalize(msisdn):
    '''Converts msisdn to 234 format'''
    return msisdn.strip()[-10:]

def clean_msisdn(msisdn):
    patt = re.compile('\+?\d+')
    match = patt.match(str(msisdn))
    if match:
        msisdn = normalize(match.group())
        if len(msisdn) not in [10, 13]:
            raise ValidationError('incorrect length of %s' % msisdn)
        #if msisdn[:-7] not in settings.AIRTEL_PREFIX:
        #    raise ValidationError('%s is not a valid Airtel Number' % msisdn)
        return msisdn
    else:
        raise ValidationError('%s is not a valid msisdn' % msisdn)
