from __future__ import absolute_import
import datetime
from celery.task.base import periodic_task
from django.core.mail import send_mail
from celery import task
import os, re
from newunica.utils import logger
from django.conf import settings
from datetime import datetime
from celery.task.schedules import crontab
from datautils import txt
from newunica.smsgw import *
import redis
from campaign.models import Broadcast

'''
@periodic_task(run_every=datetime.timedelta(seconds=30))
def email_sending_method():
    send_mail("i am coming")
'''


@task
def print_all():
    logger.info("I am man hjvslbsv;vdsjbkflblvjdlsj,k")
    print "ayanfe"


# @periodic_task(run_every=crontab(minute="*/30"))
# def delete_all():
#    try:
#        start = datetime.now()
#        FilterationBatch.objects.all().delete()
#        _new_file_path = os.path.join(settings.FILTERED_BACTHES_FILE_LOCATION, "processed/*")
#        os.remove(_new_file_path)
#        logger.info('done in %s seconds' % (datetime.now()- start))
#    except Exception, ex:
#        logger.debug(str(ex))

# def subs_info(segment):
#     try:
#         db = cx_Oracle.connect(
#             'dndsms/sms$dnd123@(DESCRIPTION=(ADDRESS_LIST=(ADDRESS=(PROTOCOL=TCP)(HOST=smadb-scan)(PORT=1549)))(CONNECT_DATA=(SERVICE_NAME=SMADB)))')
#     except Exception, exc:
#         logger.error('could not connect to db. Details: %s ' % exc)
#         raise
#     else:
#         sql = "SELECT MSISDN FROM SUBSCRIBERS_OPTIN inner JOIN SUBSCRIBERS_SUBSCRIBER on MSISDN_ID=SUB_ID inner join SUBSCRIBERS_SEGMENTMENU on segment_id=id where NAME='%s'" % segment
#         cur = db.cursor()
#         logger.info(sql)
#         try:
#             _res = cur.execute(str(sql))
#         except Exception, exc:
#             logger.error('could not execute: %s' % str(exc))
#             raise
#         result = _res.fetchall()
#         msisdns = []
#         for row in result:
#             msisdns.append('234%s' % row[0])
#         return msisdns


def set_dif(filter_msisdn, dnd_msisdn):
    """

    :param filter_msisdn:
    :param dnd_msisdn:
    :return:
    """
    final = set(filter_msisdn).difference(dnd_msisdn)
    return final


def get_requests(store, key, max_count):
    """

    :param store:
    :param key:
    :param max_count:
    :return:
    """
    count = 0
    while count < max_count:
        line = store.spop(key)
        if line:
            yield line
            count +=1
        else:
            return


@task
def send_campaign(sender, message, key, flash=1, pk=None):
    """

    :param sender:
    :param message:
    :param key:
    :param flash:
    :param pk:
    :return:
    """

    new_file_path = os.path.join(settings.FILTERED_BACTHES_FILE_LOCATION, "%s" % key)
    background_filter(key, new_file_path)
    _obj = SMSGW("172.24.6.103", "8aB4wnwfn7Fj?ZB", key, flash)
    store = _obj.store()
    print "ayanfe"
    for line in get_requests(store, key, store.scard(key)):
        try:
            print line
            _obj.send_sms(sender, line.strip(), message, flash)
            #store.sadd("PROCESSED_SUBSCRIPTION_%s" % key, line)
            logging.info("%s" % line.strip())
        except Exception, ex:
            logging.error("An error occured! please try again later %s " % str(ex))
            store.sadd(key, line.strip())
            pass
    Broadcast.objects.get(pk=pk).update(status='Completed')


def process_file(filename, filepath):
    """

    :param filename:
    :param filepath:
    :return:
    """

    logger.debug("%s | %s" % (filename, filepath))
    store = redis.Redis(settings.REDIS_SERVER, password=settings.REDIS_PASS)
    try:
        file = open(filepath, 'r')
        _data = txt.extract(file.read())
        data = set(_data)
        if len(data) == 0:
            logger.info('The file is empty')
    except Exception, exc:
        logger.error('error extracting file: %s' % str(exc))
    patt = re.compile('\+?\d+')
    num_errors = []
    msisdns = set()
    off_net = []
    incomplete = []
    for row in data:
        match = patt.match(str(row.strip()))
        # logger.info(match)
        if match:
            msisdn = normalize(match.group())
            if len(msisdn) not in [10, 13]:
                incomplete.append(msisdn)
                continue
            msisdns.add(msisdn)
            store.sadd(filename, msisdn)
        else:
            # invalid msisdn
            num_errors.append(row)
    logger.info("Error: %s, Success: %s" % (len(num_errors), len(msisdns)))


def background_filter(new_file_name, new_file_path):
    """

    :param new_file_name:
    :param new_file_path:
    :return:
    """
    try:
        logger.info('starting...')
        start = datetime.now()
        store = redis.Redis('172.24.6.103', password='8aB4wnwfn7Fj?ZB')
        #msisdns = process_file(new_file_name, _filename)
        try:
            file = open(new_file_path, 'r')
            _data = txt.extract(file.read())
            data = set(_data)
            if len(data) == 0:
                logger.info('The file is empty')
        except Exception, exc:
            logger.error('error extracting file: %s' % str(exc))
        for row in list(data):
            print '%s|%s' % (row, new_file_name)
            store.sadd(new_file_name, row)
        logger.info('newpath:%s , file_name:%s' % (new_file_path, new_file_name))
        logger.info('done in %s seconds' % (datetime.now() - start))
    except Exception, ex:
        logger.debug(str(ex))


def normalize(msisdn):
    '''Converts msisdn to 234 format'''
    return '234%s' % msisdn.strip()[-10:]

