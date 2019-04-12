from django import forms
from models import *
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from datautils import txt
import re, os
from newunica.utils import logger


class DateInput(forms.DateInput):
    input_type = 'date'


class BroadcastForm(forms.ModelForm):

    class Meta:
        model = Broadcast
        exclude = ['user', 'recipient_count', 'date_created']

        widgets = {
            'broadcast_name': forms.TextInput(attrs={'class': 'form-control', 'required':'required'}),
            # 'broadcast_description': forms.TextInput(attrs={'class': 'form-control'}),
            'broadcast_description': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'sender':forms.TextInput(attrs={'class': 'form-control', 'required':'required'}),
            'content_type': forms.Select(choices=CONTENT_TYPE, attrs={'class': 'form-control'}),
            #'base_file': forms.ModelChoiceField(queryset=Uploads.objects.filter(user=user),attrs={'class': 'form-control', 'required': 'required', 'v-model': 'base_file'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', 'placeholder': _('Enter Message')}),
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        user = kwargs.pop('place_user')
        super(BroadcastForm, self).__init__(*args, **kwargs)
        print user
        # there's a `fields` property now
        # self.fields['center_code'].required = False
        self.fields['base_file'].queryset = Uploads.objects.filter(user=user)


def normalize(msisdn):
    '''Converts msisdn to 234 format'''
    return '234%s' % msisdn.strip()[-10:]


class UploadsForm(forms.ModelForm):

    class Meta:
        model = Uploads
        exclude = ['user', 'date_created']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'required':'required'}),
            # 'broadcast_description': forms.TextInput(attrs={'class': 'form-control'}),
            'name_id': forms.TextInput(attrs={'class': 'form-control', 'required':'required'}),
            'recipient_count' : forms.TextInput(attrs={'class': 'form-control', 'required':'required'})

        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UploadsForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        # self.fields['center_code'].required = False
        #self.fields['base_file'].queryset = Uploads.objects.all()


