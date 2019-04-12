import logging
import os
import urllib, urllib2
import uuid
import redis
from django.conf import settings
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from newunica.settings import SITE_URL
import smtplib
from flight.models import ApprovalMapping, Travel,FunctionalHead,Advance,AdvanceDescription, Trip
import json
from utility.models import StaffList

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'travel.log')

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


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def import_module(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod




#
# from django import http
# from django.shortcuts import render_to_response
# from django.template.loader import get_template
# from django.template import Context
# import xhtml2pdf.pisa as pisa
try:
    import StringIO
    StringIO = StringIO.StringIO
except Exception:
    from io import StringIO
import cgi


def fetch_resources(uri, rel):
    import os.path
    from django.conf import settings
    path = os.path.join(
            settings.MEDIA_ROOT,
            uri.replace(settings.MEDIA_URL, ""))
    return path

def check_existing_account(user, receiver_type):
    """
        This method is to check if the corresponding user has the col as in the excel sheet
    """
    #query user object where user = user
    user = user
    return user


def send_email(subject='', template='', to=[], from_email='', context_dict={}):
    #send mail
    #body = render_to_string(template, context_dict)
    #msg = EmailMessage(subject=subject, body=body, to=to, from_email=from_email)
    #msg.content_subtype = "html"
    #return msg.send(fail_silently=True)

    body = render_to_string(template, context_dict)
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = 'traveldesk@ng.airtel.com'
    msg['Reply-to'] = 'please do not replay to this email.'
    msg['message'] = body
    part = MIMEText(body, 'html')
    #part = MIMEApplication(open(LOGFILE,"rb").read())
    #part.add_header('Content-Disposition', 'attachment', filename='file.txt')
    msg.attach(part)
    server = smtplib.SMTP("10.56.131.8:25")
    #server = smtplib.SMTP("127.0.0.1:2525")
    res = server.sendmail(msg['From'], to , msg.as_string())


def my_random_string(string_length=6):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4())
    random = random.upper()
    random = random.replace("-","")
    return 'AT%s' % random[0:string_length]


def get_details(uid):
    try:
       obj = StaffList.objects.get(auid=uid)
       email = obj.email
       name = obj.name
    except StaffList.DoesNotExist:
       email = 'adegoke.ayanfe@ng.airtel.com'
       name = 'ayanfe'
    return '%s,%s' % (email, name)


road_map_list = ['line_manager', 'functional_head', 'cco', 'hrd', 'travel_desk', 'budget_team', 'payable_account']
national_map_list = ['line_manager', 'functional_head', 'cco', 'hrd','ceo', 'travel_desk', 'budget_team', 'payable_account']
international_map_list = ['line_manager', 'functional_head', 'cco', 'hrd', 'ceo', 'travel_desk', 'budget_team', 'payable_account']
training_map_list = ['line_manager', 'functional_head', 'cco', 'talent_team', 'hrd', 'ceo', 'travel_desk', 'budget_team', 'payable_account']
ec_map_list = ['hrd', 'ceo', 'travel_desk', 'budget_team', 'payable_account']


def workflow_trip_mapping(employee, ref, req=0):
    #import pdb
    # pdb.set_trace()
    travel = Travel.objects.get(reference=ref)
    store = redis.Redis(settings.REDIS_SERVER, 8091)
    store.sadd(settings.APPROVAL_KEY, ref)
    r = ''
    i = ''
    map_list = []
    num_results = FunctionalHead.objects.filter(name=travel.user).count()
    if num_results >= 1:
        map_list = ec_map_list
    elif travel.purpose == 'Training':
        map_list = training_map_list
    elif travel.trip_type == 'Road Trip':
        map_list = road_map_list
    elif travel.travel_type == 'National':
        map_list = national_map_list
    elif travel.travel_type == 'International':
        map_list = international_map_list
    logger.info('%s requested for approval with %s workflow' % (travel.user, map_list))
    for i in map_list:
        field_name = i
        obj = ApprovalMapping.objects.get(employee=travel.user)
        r = getattr(obj, field_name)
        #get current value index, if less than index value approval from db, break loop and move to next loop
        person_index = map_list.index(travel.approval_level)
        curr_loop = map_list.index(i)
        logger.info('%s approval level is with %s' % (travel.user, field_name))
        next_person_index = person_index + 1
        if person_index > curr_loop:
            continue
        elif travel.approval_status == 'Completed':
            logger.info('End of workflow with last approval is %s' % travel.approval_level)
            subject = 'Travel Request | Airtel Travel'
            email_template = 'flight/final_email.html'
            advance = Advance.objects.filter(travel=travel.pk)
            travel.reference=my_random_string(6)
            travel.approval_level = 'Completed'
            travel.save()
            to = travel.user.email #'adegokeayanfe@gmail.com'  # map_list[next_person_index]  # change this part to the conrresponding email (e.g: line manager email)
            from_email = "Airtel Travel <traveldesk@airtel.ng>"
            context_dict = {'travel': travel, 'user': employee, 'host': SITE_URL }
            send_email(subject, email_template, [to, ], from_email, context_dict)
            break
        elif travel.approval_level == map_list[-1] and travel.approval_status not in ('Completed', 'Finished'):
            travel.reference = my_random_string(6)
            subject = 'Travel Request | Airtel Travel'
            email_template = 'flight/approval-request.html'
            travel.approval_status = 'Completed'
            travel.save()
            advance = Advance.objects.filter(travel=travel.pk)
            location = Trip.objects.filter(travel=travel.pk)
            approval_person = get_details(next_person_value).split(',')
            to = approval_person[0]  #'adegokeayanfe@gmail.com' #map_list[next_person_index]  # change this part to the conrresponding email (e.g: line manager email)
            #to = 'adegokeayanfe@gmail.com'
            from_email = "Airtel Travel <traveldesk@ng.airtel.com>"
            context_dict = {'travel': travel, 'location': location, 'advances': advance, 'user': employee, 'host': SITE_URL, 'name': approval_person[1].title()}
            send_email(subject, email_template, [to, ], from_email, context_dict)
            break
        if person_index == curr_loop and req == 1: #this approval person is the current person approving the request, save and update db to the next person that is not null
            #req=1 because it came from an approval or reject link, not from form filling on app by user
            #look up next person that isnt null
            #if len(map_list)
            next_person = map_list[next_person_index]
            next_person_value = getattr(obj, next_person)
            if next_person_value is not None and next_person_value != '':
                next_person_check = map_list[person_index]
                last_person_back = map_list[person_index - 1]
                next_person_current_value = getattr(obj, next_person_check)
                last_person_current_value = getattr(obj, last_person_back)
                #print next_person_current_value
                if next_person_current_value == next_person_value:
                    travel.approval_level = map_list[next_person_index + 1]
                    logger.info('new map listing %s' % map_list[next_person_index + 1])
                    continue
                elif last_person_current_value == next_person_value:
                    travel.approval_level = map_list[next_person_index + 0]
                    logger.info('new map listing %s hhhh' % map_list[next_person_index + 1])
                    continue
                logger.info('show me %s - %s' % (map_list[next_person_index], map_list[-1]))
                #if map_list[next_person_index] == map_list[-1]:
                #    travel.reference = my_random_string(6)
                #    subject = 'Travel Request | Airtel Travel'
                #    email_template = 'flight/approval-request.html'
                #    travel.approval_status = 'Completed'
                #    travel.save()
                #    advance = Advance.objects.filter(travel=travel.pk)
                #    location = Trip.objects.filter(travel=travel.pk)
                #    approval_person = get_details(next_person_value).split(',')
                #    to = approval_person[0]  #'adegokeayanfe@gmail.com' #map_list[next_person_index]  # change this part to the conrresponding email (e.g: line manager email)
                #    #to = 'adegokeayanfe@gmail.com'
                #    from_email = "Airtel Travel <travel@ng.airtel.com>"
                #    context_dict = {'travel': travel, 'location': location, 'advances': advance, 'user': employee, 'host': SITE_URL, 'name': approval_person[1].title()}
                #    send_email(subject, email_template, [to, ], from_email, context_dict)
                #    break
                travel.approval_level = map_list[next_person_index]
                travel.reference = my_random_string(6)
                subject = 'Travel Request | Airtel Travel'
                email_template = 'flight/approval-request.html'
                advance = Advance.objects.filter(travel=travel.pk)
                location = Trip.objects.filter(travel=travel.pk)
                approval_person = get_details(next_person_value).split(',')
                to = approval_person[0]  #'adegokeayanfe@gmail.com' #map_list[next_person_index]  # change this part to the conrresponding email (e.g: line manager email)
                #to = 'adegokeayanfe@gmail.com'
                from_email = "Airtel Travel <travel@ng.airtel.com>"
                context_dict = {'travel': travel, 'location': location, 'advances': advance, 'user': employee, 'host': SITE_URL, 'name': approval_person[1].title()}
                send_email(subject, email_template, [to, ], from_email, context_dict)
                #if travel.approval_level == map_list[-1]:
                #    travel.approval_status='last_entry'
                logger.debug('%s Approval Email sent to %s-%s' % (travel.user, to, next_person_value))
                break
            else:
                next_person_index += 1
                next_person = map_list[next_person_index]
                next_person_value = getattr(obj, next_person)
                while next_person_value is not None:
                    travel.approval_level = map_list[next_person_index]
                    travel.reference = my_random_string(6)
                    subject = 'Travel Request | Airtel Travel'
                    email_template = 'flight/approval-request.html'
                    advance = Advance.objects.filter(travel=travel.pk)
                    approval_person = get_details(next_person_value).split(',')
                    location = Trip.objects.filter(travel=travel.pk)
                    to = approval_person[0]
                    #to = 'adegokeayanfe@gmail.com' #map_list[next_person_index]  # change this part to the conrresponding email (e.g: line manager email)
                    from_email = "Airtel Travel <travel@ng.airtel.com>"
                    context_dict = {'travel': travel,'location': location, 'advances': advance, 'user': employee, 'host': SITE_URL, 'name':approval_person[1].title()}
                    send_email(subject, email_template, [to, ], from_email, context_dict)
                    #if travel.approval_level == map_list[-1]:
                    #   travel.approval_status='last_entry'
                    logger.debug('Second loop %s approval email sent to %s-%s' % (travel.user, to, next_person_value))
                    break
            break

        if r is not None and r !='':#there is a value in model field, send mail to the value
            #pdb.set_trace()
            '''
            print 'which one'
            next_person_value = getattr(obj, map_list[next_person_index])
            next_person_check = map_list[person_index]
            last_person_back = map_list[person_index - 1]
            next_person_current_value = getattr(obj, next_person_check)
            last_person_current_value = getattr(obj, last_person_back)
            if next_person_current_value == next_person_value:
                travel.approval_level = map_list[next_person_index + 1]
                print 'new map listing %s' % map_list[next_person_index + 1]
                continue
            elif last_person_current_value == next_person_value:
                travel.approval_level = map_list[next_person_index + 1]
                print 'new map listing %s hhhh' % map_list[next_person_index + 1]
                continue
            '''
            # look up approval person's id(assume as mail and send mail)
            travel.approval_level = i
            travel.reference = my_random_string(6)
            subject = 'Travel Request | Airtel Travel'
            email_template = 'flight/approval-request.html'
            advance = Advance.objects.filter(travel=travel.pk)
            approval_person = get_details(r).split(',')
            location = Trip.objects.filter(travel=travel.pk)
            #to = 'adegokeayanfe@gmail.com'
            to = approval_person[0] #'adegokeayanfe@gmail.com' #r  # change this part to the conrresponding email (e.g: line manager email)
            from_email = "Airtel Travel <travel@ng.airtel.com>"
            context_dict = {'travel': travel, 'location': location, 'advances': advance, 'user': employee, 'host': SITE_URL, 'name': approval_person[1].title()}
            send_email(subject, email_template, [to, ], from_email, context_dict)
            logger.debug('This is the first email sent for approval for %s , Approval Email sent to %s' % (travel.user, to))
            break
        else:#move to the next value, whether approval person is null or approval person has approved update model row too
            print 'move to the next approval'
            logger.debug('moving to the next approval loop')
            travel.approval_level = i
    travel.save()
    return r


#if __name__=='__main__':
#    generate_sms_pin()
