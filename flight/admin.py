from django.contrib import admin
from models import *
from django.http import HttpResponse
import csv
# Register your models here.


class TravelAdmin(admin.ModelAdmin):
    list_display = ['user', 'ticket_no', 'function','showTeam', 'showAdvance', 'showAccomodation','cost_code', 'travel_type', 'trip_type', 'band', 'purpose', 'date_created']
    search_fields = ['user__username', 'ticket_no']
    date_hierarchy = ('date_created')
    list_filter = ('date_created', 'status')
    actions = ['download_selected', ]

    def download_selected(self, request, queryset):
         headers = ['user', 'reference', 'function', 'travel_type', 'trip_type', 'band', 'purpose', 'center_code',
                    'advance_total_naira', 'estimated_cost_naira', 'advance_total_dollar', 'estimated_cost_dollar', 'objective', 'approval_level','date_created']
         response = HttpResponse(content_type='text/csv')
         response['Content-Disposition'] = 'attachment;filename=Travel.csv'
         writer = csv.writer(response)
         writer.writerow([header.upper() for header in headers])
         for obj in queryset:
             line = []
             for header in headers:
                line.append(getattr(obj, header))
             writer.writerow(line)
         return response


class ApprovalMappingAdmin(admin.ModelAdmin):
    list_display = ('employee', 'line_manager', 'functional_head', 'cco', 'talent_team','hrd', 'ceo','travel_desk', 'budget_team', 'payable_account')
    search_fields = ('employee', 'line_manager')


class ApprovalsAdviceAdmin(admin.ModelAdmin):
    list_display = ('ticket_no', 'reference','approval_person', 'approval_person_name', 'approval_person_email', 'is_approved','approval_person_level', 'status')
    search_fields = ('travel__ticket_no','reference', 'approval_person')
    list_filter = ('is_approved', 'status')

    
class TravelAdviceAdmin(admin.ModelAdmin):
    list_display = ('travel','location_name', 'hotel_name', 'address')


class AdvanceAdmin(admin.ModelAdmin):
    list_display = ('travel', 'advance_description', 'units', 'rate', 'cost', 'currency')
    search_fields = ['travel__user__username']


# class ApprovalAdmin(admin.ModelAdmin):
#     list_display = ('employee', 'line_manager', 'functional_head', 'cco')

admin.site.register(ApprovalMapping, ApprovalMappingAdmin)
admin.site.register(Travel, TravelAdmin)
admin.site.register(Advance, AdvanceAdmin)
admin.site.register(TravelAdvice, TravelAdviceAdmin)
admin.site.register(Approvals, ApprovalsAdviceAdmin)