from __future__ import unicode_literals
import psycopg2
import os
import logging
from datetime import date, datetime
import urllib, urllib2
import sys
from random import random
import redis
from django.conf import settings


LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'emautils.log')
LOG_FILE = os.path.join('Loggile-%s.log' % date.today())
#LOG_FILE = '/var/db/smsgw/SMSGW-%s.log' % date.today()
#PID_FILE = '/var/db/smsgw/SMSG.PID'
logger = logging.getLogger('smsgw')
handler = logging.FileHandler(LOG_FILE)
formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


AIR_SERVER_URIS = [
                    #'http://172.24.6.103:15495/cgi-bin/sendsms?',
                    'http://172.24.6.103:15493/cgi-bin/sendsms?',
                    'http://172.24.6.103:15498/cgi-bin/sendsms?',
                    #'172.24.165.82:10010/Air'
                    ]


username='test'
password='test123'

class SMSGW():

    def __init__(self, host, password, key, flash):
        self.redis_host = host
        self.password = password
        self.key = key
        self.flash = flash

    def store(self):
        return redis.Redis(host=self.redis_host, password=self.password)

    def get_air_server(self):
        'Get all airservers'
        return AIR_SERVER_URIS[int(random() * len(AIR_SERVER_URIS))]

    # def message_sms(self):
    #     mess = {k: self.store().hget(self.key, k) for k in self.store().hkeys(self.key)}
    #     return mess
    #
    # def sender_sms(self):
    #     mess = {k: self.store().hget(self.sender, k) for k in self.store().hkeys(self.sender)}
    #     return mess

    def send_sms(self, short_code, msisdn, msg, flash):
        '''
        Send message to subscriber using short_code
        '''
        to = '234%s' % msisdn[-10:]
        sms_url = self.get_air_server()
        params = {
                'from' :short_code,
                'text': msg,
                'to':'234%s' % msisdn[-10:],
                'username': username,
                'password' : password,
                'mclass' : flash
                }
        url = sms_url + urllib.urlencode(params)
        try:
            logger.info('%s, invoking: %s' % (msisdn, url))
            response = urllib2.urlopen(url)
        except Exception, exc:
            logger.error('url: %s, error: %s' % (
                url, str(exc)))
        else:
            logger.info('msisdn: %s, response: %s' % (to, response.read()))


if __name__ == '__main__':
    _obj = SMSGW("172.24.6.103", "8aB4wnwfn7Fj?ZB")
    print _obj.message_sms()
    #print _obj.get_air_server()




# class MyDaemon(Daemon):
#     def run(self):
#         logger.info('starting...')
#         start = datetime.now()
#
#         logger.info('done in %s seconds'%(datetime.now()-start))
#         #send_sms(recipient, 'Barring done')

# if __name__ == '__main__':
#     daemon = MyDaemon(PID_FILE, stdout=LOG_FILE, stderr=LOG_FILE)
#     if len(sys.argv) == 2:
#         if sys.argv[1] in ['start', 'stop', 'restart']:
#             cmd = sys.argv[1]
#             getattr(daemon, cmd)()
#             sys.exit(0)
#     else:
#         print 'usage: %s start|stop|restart' % sys.argv[0]
#         sys.exit(2)