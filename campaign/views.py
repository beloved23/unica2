# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
import redis
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from forms import BroadcastForm, UploadsForm
from models import Broadcast
from datetime import datetime, date
from django.contrib import messages
# Create your views here.
import uuid
import os
from models import Uploads
from django.conf import settings
from datautils import txt
from newunica.utils import logger
from newunica.utils import clean_data
import json
from django.contrib.auth.models import User
from task import background_filter, send_campaign
from dateutil.parser import parse

CONT = {'Flash': 0, 'Text': 1}


class CreateBroadcast(LoginRequiredMixin, CreateView):
    model = Broadcast
    form_class = BroadcastForm

    def get_form_kwargs(self):
        kwargs = super(CreateBroadcast, self).get_form_kwargs()
        kwargs.update({'place_user': self.request.user})
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        #form.instance.job = Travel.objects.get(pk=self.kwargs['pk'])
        form.save()
        #messages.success(self.request, 'Your ticket id has been created, kindly fill the trip details!')
        return super(CreateBroadcast, self).form_valid(form)

    def get_success_url(self):
        return reverse('broadcast:add_broadcast', args=(self.object.id,))


class CreateUploads(LoginRequiredMixin, CreateView):
    model = Uploads
    form_class = UploadsForm
    success_url = '/campaign/upload'

    def form_valid(self, form):
        form.instance.user = self.request.user
        #form.instance.job = Travel.objects.get(pk=self.kwargs['pk'])
        form.save()
        messages.success(self.request, 'Base has been uploaded!')
        return super(CreateUploads, self).form_valid(form)
    # def get_success_url(self):
    #     return reverse('broadcast:upload_list')


@login_required
def upload(request, template='campaign/uploads_form.html'):
    send_campaign.delay('Bonus', 'Thanks', 'f77e4ba6-5769-11e9-a604-8c8590b996ed', 1)
    # context = {}
    # return render(request, template, context)
    return HttpResponse("Testing")


#celery -A campaign worker -l info


# class BroadcastDetail(LoginRequiredMixin, DetailView):
#     model = Broadcast

class BroadList(LoginRequiredMixin, ListView):
    dt = date.today()
    model = Broadcast

    def get_queryset(self):
        qs = super(BroadList, self).get_queryset()
        if self.request.user.is_superuser:
            return qs.order_by("-date_created")
        return qs.filter(referrer=self.request.user).order_by("-date_created")

#{"broadcast_name":"Hello","broadcast_description":"Voice spot","sender":"Bonus+","message":"Thanks","base_file":"1","user":"1"}


@csrf_exempt
def createBroadcast(request):
    username = request.user.username
    if request.method == 'POST':
        result = json.loads(request.body.decode('utf-8'))
        try:
            # import pdb
            # pdb.set_trace()
            user = User.objects.get(pk=result['user'])
            broadcast_name = result['broadcast_name']
            broadcast_description = result['broadcast_description']
            sender = result['sender']
            message = result['message']
            content_type = result['content_type']
            #schedule_start = result['schedule_start']
            schedule_start = parse(result['schedule_start']).strftime('%Y-%m-%d %H:%M:%S')
            end_time =  parse(result['end_time']).strftime('%Y-%m-%d %H:%M:%S')
            base_file = Uploads.objects.get(pk=result['base_file'])
            print schedule_start
            print end_time
            Broadcast.objects.create(
                user=user,
                broadcast_name=broadcast_name,
                broadcast_description=broadcast_description,
                sender=sender,
                base_file=base_file,
                message=message,
                content_type=content_type,
                status="Pending"
            )

            # if schedule_start is None or '':
            #     Broadcast.objects.create(
            #         user=user,
            #         broadcast_name=broadcast_name,
            #         broadcast_description=broadcast_description,
            #         sender=sender,
            #         base_file=base_file,
            #         message=message,
            #         content_type=content_type,
            #         status="Pending"
            #          )
            # else:
            #     Broadcast.objects.create(
            #         user=user,
            #         broadcast_name=broadcast_name,
            #         broadcast_description=broadcast_description,
            #         sender=sender,
            #         base_file=base_file,
            #         message=message,
            #         content_type=content_type,
            #         #schedule_start=schedule_start,
            #         #end_date=end_time,
            #         status="Pending"
            #     )
            print base_file.name_id
            taskid = send_campaign.delay(sender, message, base_file.name_id, CONT[content_type])
            logger.info("TaskId %s" % taskid)
            res = {'action': True, "message": "Campaign created!"}
        except Exception, ex:
            logger.error("Error processing rquest %s-%s" % (str(ex), username))
            res = {'action': False, "message": "Travel request created"}
        return HttpResponse(json.dumps(res), content_type='application/json')
    raise PermissionDenied


@csrf_exempt
def import_report(request):
    if request.method == 'POST':
        print request.FILES
        # started = datetime.datetime.now()
        #form = UploadsForm(request.POST, request.FILES)
        try:
            _file_name = request.FILES['file[0]'].name
            print _file_name
            data = txt.extract(request.FILES['file[0]'].read())
            data = set(data)
            new_msisdns = clean_data(data)
            new_file_name = uuid.uuid1()
            new_file_path = os.path.join(settings.FILTERED_BACTHES_FILE_LOCATION, "%s" % new_file_name)
            _sfile = open(new_file_path, 'wb+')
            [_sfile.write('%s\n' % chunk) for chunk in new_msisdns]
            _sfile.close()
            res = {"Message": "%s" % new_file_name, "Count": len(new_msisdns)}
            #task_id = background_filter.delay(new_file_name, new_file_path)
            #logger.info("Task Id: %s for %s" % (task_id, new_file_name))
            # #messages.info(request, "Your file (%s) has been queued, pls check back to download" % _file_name)
        except Exception, ex:
            #print str(ex)
            logger.info("Error %s" % str(ex))
            res = {"Message": "NoApplied", "Count": 0}
    return HttpResponse(json.dumps(res), content_type='application/json')
