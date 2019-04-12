from django.core.signing import Signer
from django.db import models
from django.contrib.auth.models import User
#from utility.models import *


# class UserProfile(models.Model):
#      user = models.OneToOneField(User, null=False, blank=False, related_name='user_profile')
#      phone = models.CharField(max_length=15, null=True, unique=True, blank=True)
#
#      def __unicode__(self):
#          return self.user.username
#

# {
#   "aauid": "2323284",
#   "fullName": "Chiamaka Ojukwu",
#   "email": "chiamaka.ojukwu@ng.airtel.com",
#   "delegateEmail": "adeniyi.adebanjo@ng.airtel.com",
#   "startDate": "2018-03-22 16:32:37",
#   "endDate": "2018-03-26 16:32:37",
# }


# class DelegateApproval(models.Model):
#     user = models.ForeignKey(User)
#     fullname = models.CharField(max_length=50, null=True)
#     delegate_email = models.CharField(max_length=50, null=False, blank=False)
#     start_date = models.DateTimeField(null=True)
#     end_date = models.DateTimeField(null=True)
#
#     def __unicode__(self):
#         return self.fullname


