# from __future__ import unicode_literals
#
# from django.db import models
# from django.contrib.auth.models import User
# from django.core.validators import RegexValidator
# from datetime import datetime, date
# from django.conf import settings
# from utility.models import ZONE
#
# from utility.models import *
# # Create your models here.
#
# STATUS = (
#     ('Pending','Pending'),
#     ('Completed', 'Completed')
# )
#
# ACCOMMODATION_TYPE = (
#     ('Hotel', 'Hotel'),
#     ('Lieu', 'Lieu')
# )
#
# MEAL_DAYS = ((str(i), i) for i in range(0, 31))
#
# TRAVEL_TYPE = (('National', 'National'),
#                ('International', 'International'))
#                #('Private', 'Private'))
#
# TRIP_TYPE = (
#                ('One Way Flight', 'One Way Flight'),
#                ('Return Flight', 'Return Flight'),
#                ('Multiple Flight', 'Multiple Flight'),
#                ('Road Trip', 'Road Trip')
#                )
#
# ACCOUNT_TYPES = {'line_manager': 'Line Manager', 'functional_head': 'Functional Head', 'cco': 'CCO', 'hrd': 'HRD',
#                  'travel_desk': 'Travel Desk', 'budget_team': 'Budget Team', 'payable_account': 'Payable Account'}
#
# ACCOUNT_TYPES_LIST = ['Line Manager', 'Functional Head', 'CCO', 'Travel Desk', 'Budget Team', 'Payable Account']
#
# #
#
# APPROVAL_STATUS = (('Rejected', 'Rejected'),
#                     ('Approved', 'Approved'))
#
#
#
# class Travel(models.Model):
#     user = models.ForeignKey(User)
#     reference = models.CharField(max_length=20, null=True, blank=True)
#     ticket_no = models.CharField(max_length=20, null=True, blank=True)
#     function = models.ForeignKey(Function)
#     travel_type = models.CharField(max_length=30, choices=TRAVEL_TYPE)
#     trip_type = models.CharField(max_length=30, choices=TRIP_TYPE)
#     accommodation_type = models.CharField(choices=ACCOMMODATION_TYPE, max_length=20)
#     zone = models.CharField("Travel Zone", choices=ZONE, max_length=15, null=True)
#     band = models.ForeignKey(Band)
#     purpose = models.ForeignKey(Purpose)
#     center_code = models.CharField(max_length=20, null=True, blank=True, help_text='Cost Center code to be charged')
#     status = models.CharField(choices=STATUS, default='Pending', null=True, max_length=20)
#     advance_total_naira = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     estimated_cost_naira = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     advance_total_dollar = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     estimated_cost_dollar = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     total_naira = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     total_dollar = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     objective = models.TextField()
#     cost_code = models.CharField(max_length=20, null=True, blank=True)
#     accomodation_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     accomodation_units = models.CharField(max_length=10, blank=True, null=True)
#     flight_rate = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
#     flight_units = models.CharField(max_length=10, blank=True, null=True)
#     approval_status = models.CharField(null=True, choices=APPROVAL_STATUS, blank=True, max_length=20)
#     approval_level = models.CharField(null=True, blank=True, max_length=20)
#     is_advice = models.BooleanField(default=False)
#     f_type = models.BooleanField(default=False)
#     is_team = models.BooleanField(default=False)
#     team_len = models.CharField(max_length=20, null=True, blank=True)
#     date_created = models.DateTimeField(default=datetime.now, null=True, blank=True)
#
#     def __str__(self):
#         return '%s' % (self.ticket_no)
#
#     @models.permalink
#     def get_absolute_url(self):
#         return "travel:delete", (), {"pk": self.pk}
#
#     @models.permalink
#     def get_edit_url(self):
#         return "travel:edit_travel", (), {"pk": self.pk}
#
#     @models.permalink
#     def get_detail_url(self):
#         return "travel:travel_detail", (), {"pk": self.pk}
#
#
#     def showAdvance(self):
#         advance = Advance.objects.filter(travel=self.pk)
#         row = []
#         for i in advance:
#             row.append('%s-%s%s\n' % (i.advance_description, i.currency, i.cost))
#         return row
#
#     def showAccomodation(self):
#         accomodation = Accommodation.objects.filter(travel=self.pk)
#         row = []
#         for i in accomodation:
#             row.append('%s-%s%s\n' % (i.name, i.check_in_date, i.check_out_date))
#         return row
#
#     def showTeam(self):
#         team = TeamTravel.objects.filter(travel=self.pk)
#         row = []
#         for i in team:
#             row.append('%s-%s\n' % (i.email, i.name))
#         return row
#
#     def json(self):
#         return dict(
#             id=self.pk,
#             travel_type=self.travel_type,
#             trip_type=self.trip_type,
#             accommodation_type=self.accommodation_type,
#             purpose=str(self.purpose),
#             advance_total=self.advance_total,
#             estimated_cost=self.estimated_cost,
#             objective=str(self.objective),
#             approval_status=self.approval_status,
#             approval_level=self.approval_level,
#             date_created=str(self.date_created)
#
#         )
#
#
# class TeamTravel(models.Model):
#     travel = models.ForeignKey(Travel, related_name='teamtravel')
#     auuid = models.CharField(max_length=10, null=True, blank=True)
#     email = models.CharField(max_length=70, null=True, blank=True)
#     name = models.CharField(max_length=50, null=True, blank=True)
#
#     def __unicode__(self):
#         return self.auuid
#
#     def as_json(self):
#         return dict(
#             id=self.pk,
#             auuid=self.auuid,
#             email=self.email,
#             name=self.name
#         )
#
#
# class Meal(models.Model):
#     no_of_days = models.CharField(choices=MEAL_DAYS, max_length=10, null=True)
#     travel = models.ForeignKey(Travel)
#
#     def __str__(self):
#         return self.no_of_days
#
#
# class Trip(models.Model):
#     travel = models.ForeignKey(Travel)
#     departure_airport = models.CharField(max_length=150, null=True)
#     destination_airport = models.CharField(max_length=150, null=True)
#     departure_date = models.DateField(null=True, blank=True)
#     destination_date = models.DateField(null=True, blank=True)
#     mileage = models.CharField(max_length=11, null=True)
#     flight_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
#     is_return = models.BooleanField(default=False)
#     # flight_cost = models.CharField(max_length=20, null=True)
#
#     def __str__(self):
#         return str(self.departure_airport)
#
#
# APPROVAL_STAGES = (('COMPLETED', 'COMPLETED'),
#                    ('PENDING', 'PENDING'),
#                    ('EXPIRED', 'EXPIRED')
#                    )
#
#
# class Approvals(models.Model):
#     travel = models.ForeignKey(Travel, related_name="travel_approval")
#     reference = models.CharField(max_length=10, null=True, blank=True)
#     approval_person = models.CharField(max_length=10, null=True, blank=True)
#     approval_person_name = models.CharField(max_length=50, null=True, blank=True)
#     approval_person_level = models.CharField(max_length=50, null=True, blank=True)
#     approval_person_email = models.CharField(max_length=50, null=True, blank=True)
#     is_approved = models.BooleanField(default=False)
#     status = models.CharField(choices=APPROVAL_STAGES, max_length=10, null=True)
#     date_created = models.DateTimeField(default=datetime.now, null=True, blank=True)
#
#     class Meta:
#         verbose_name = 'Approval'
#         #ordering = ('-pk', )
#
#     def __str__(self):
#         return self.approval_person
#
#     def ticket_no(self):
#         return self.travel.ticket_no
#
#     def as_json(self):
#         return dict(
#                id=self.pk,
#                reference=self.reference,
#                ticket=self.travel.ticket_no,
#                approval_person=self.approval_person,
#                approval_person_level=self.approval_person_level,
#                url=str(self.travel.get_detail_url()),
#                approval_person_name=self.approval_person_name,
#                status=self.status,
#                firstname=self.travel.user.first_name,
#                lastname=self.travel.user.last_name,
#                is_approved='APPROVED' if self.is_approved else 'REJECTED',
#                color='success' if self.is_approved else 'danger',
#                host=settings.SITE_URL,
#                date_created=str(self.date_created.strftime('%Y-%m-%d %H:%M:%S %p'))#   ('%H-%m-%S %p %d-%m-%Y'))
#         )
#
#
#
# class TravelAdvice(models.Model):
#     travel = models.ForeignKey(Travel)
#     location_name = models.CharField(max_length=150, null=True)
#     hotel_name = models.CharField(max_length=50, null=True)
#     address = models.CharField(max_length=200, null=True)
#
#     def __str__(self):
#         return self.location_name
#
#
# class Accommodation(models.Model):
#     travel = models.ForeignKey(Travel)
#     name = models.CharField(max_length=50, blank=True)
#     check_in_date = models.DateField(null=False)
#     check_out_date = models.DateField(null=False)
#
#     def __str__(self):
#         return self.name
#
# #import pdb
# #pdb.set_trace()
#
# CURRENCY = (
#     ('USD', 'USD'),
#     ('NAIRA', 'NAIRA')
# )
#
#
# class Advance(models.Model):
#     travel = models.ForeignKey(Travel)
#     advance_description = models.ForeignKey(AdvanceDescription, related_name='advance_des')
#     units = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
#     rate = models.CharField(max_length=10, validators=[RegexValidator(r'^\d{1,10}$')])
#     cost = models.DecimalField(max_digits=10, decimal_places=2, null=True)
#     currency=models.CharField(choices=CURRENCY,max_length=10, null=True)
#
#     def __str__(self):
#         return self.units
#
#
# APPROVAL_STATUS = (
#     ('Approved', 'Approved'),
#     ('Rejected', 'Rejected')
# )
#
# class ApprovalMapping(models.Model):
#     employee = models.CharField(max_length=10, null=False)
#     line_manager = models.CharField(max_length=10, null=True, blank=True)
#     functional_head = models.CharField(max_length=10, null=True, blank=True)
#     cco = models.CharField(max_length=10, null=True, blank=True)
#     talent_team = models.CharField(max_length=10, null=True, blank=True)
#     hrd = models.CharField(max_length=10, null=True, blank=True)
#     ceo = models.CharField(max_length=10, null=True, blank=True)
#     travel_desk = models.CharField(max_length=10, null=True, blank=True)
#     budget_team = models.CharField(max_length=10, null=True, blank=True)
#     payable_account = models.CharField(max_length=10, null=True, blank=True)
#     approval_status = models.CharField(choices=APPROVAL_STATUS, null=True, blank=True, max_length=30)
