from django.shortcuts import render
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
#from models import UserProfile
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from newunica.helper import is_verified_required
from django.contrib.auth.models import User
from .forms import UserLoginForm #CompleteProfileForm
import json
from django.http import HttpResponse
# from newunica.utils import delegate_approval
import requests
from django.conf import settings
# from newunica.utils import logger, delegate_deactivation_util
from django.core.exceptions import PermissionDenied
import datetime
# Create your views here.


def handler404(request):
    response = render_to_response('account/404.html', {},
                                  RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('account/500.html', {},
                                  RequestContext(request))
    response.status_code = 500
    return response


def logout(request):
    auth_logout(request)
    response = redirect('account:login')
    return response


@never_cache
def home(request):
    return redirect('account:login')


# @login_required
# def approval(request):
#     approval = Approvals.objects.filter(approval_person=request.user.username).order_by('-date_created')
#     #completed = approval.filter(approval_person=request.user.username, status="COMPLETED")
#     #pending = approval.filter(approval_person=request.user.username, status="PENDING")
#     new_data = [ob.as_json() for ob in approval]
#     return HttpResponse(json.dumps(new_data), content_type='application/json')
#
# @login_required
# def approval_my(request):
#     approval = Approvals.objects.filter(travel__user=request.user).order_by('-date_created')
#     #completed = approval.filter(approval_person=request.user.username, status="COMPLETED")
#     #pending = approval.filter(approval_person=request.user.username, status="PENDING")
#     new_data = [ob.as_json() for ob in approval]
#     return HttpResponse(json.dumps(new_data), content_type='application/json')
#

#http://172.24.2.135:5105/CRFAutomation/updateleaveapi

@login_required
def dashboard(request, template='account/dashboard.html'):
    context = {}
    # travel = Travel.objects.all()
    # road_count = travel.filter(user=request.user,trip_type='Road Trip').count()
    # one_way = travel.filter(user=request.user, trip_type='One Way Flight').count()
    # return_f = travel.filter(user=request.user, trip_type='Return Flight').count()
    # multiple = travel.filter(user=request.user, trip_type='Multiple Flight').count()
    # context = {'road_count': road_count, 'one_way': one_way, 'return_f': return_f, 'multiple': multiple}
    return render(request, template, context)

    #return redirect('travel:add_travel')

#
# @csrf_exempt
# def deactivate_delegate(request):
#     if request.method == "POST":
#         auuid = request.POST['auuid']
#         if auuid == request.user.username:
#             res = json.loads(delegate_deactivation_util(request.auuid))
#             context = {'status': True, 'message': res['message']}
#             logger.info("Deactivate delegation for %s - %s" % (request.auuid, res))
#             return HttpResponse(json.dumps(context), content_type="application/json")
#     raise PermissionDenied
#
#
#
# @csrf_exempt
# def post_delegate(request):
#     if request.method == "POST":
#         print ("GOKE")
#         name = request.POST['name']
#         email = request.POST['email']
#         start_date = request.POST['start_date']
#         end_date = request.POST['end_date']
#         #reason = request.POST['reason']
#         head = {'Content-Type': 'application/json'}
#         form_data = {
#             "aauid" : request.user.username,
#             "fullName" : '%s %s' % (request.user.first_name, request.user.last_name),
#             "email": request.user.email,
#             "delegateEmail" : email,
#             "startDate": datetime.datetime.strptime(start_date, '%Y-%m-%d').strftime('%Y-%m-%d %H:%m:%S'),
#             "endDate": datetime.datetime.strptime(end_date, '%Y-%m-%d').strftime('%Y-%m-%d %H:%m:%S')
#         }
#         logger.info("Starting to set delegate %s" % form_data)
#         response = requests.post(settings.SET_DELEGATE, json.dumps(form_data), headers=head)
#         logger.info("Request Info %s" % response)
#         if int(response.status_code) == 200:
#             context = {'message': 'Your request was successful', 'status': True}
#         else:
#             context = {'message': 'An error occurred! please try again', 'status': False}
#         return HttpResponse(json.dumps(context), content_type='application/json')
#     else:
#         return HttpResponse('Access Denied')
#         #context = {'message': 'An error occurred! please try again', 'status': False}
#         #return HttpResponse(json.dumps(context), content_type="application/json")


class LoginView(FormView):
    template_name = 'account/logim.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('home')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(self.success_url)
        return super(LoginView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        #import pdb
        #pdb.set_trace()
        auth_login(self.request, form.get_user())
        return super(LoginView, self).form_valid(form)
