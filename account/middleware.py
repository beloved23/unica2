from datetime import datetime, date, timedelta
from django.conf import settings
from newunica.utils import *
from django.contrib import auth


# class DelegateMiddleware(object):
#
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         request.auuid = request.user.username
#         res = json.loads(delegate_approval(request.user.username))
#         if res['onLeave'] in (None, 'No', ):
#            status = 'false'
#         else:
#            status = 'true'
#         request.status = status
#         response = self.get_response(request)
#         return response
