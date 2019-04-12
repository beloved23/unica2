from django import forms
from models import *
from django.utils.translation import ugettext_lazy as _


class DateInput(forms.DateInput):
    input_type = 'date'

class TravelForm(forms.ModelForm):

    class Meta:
        model = Travel
        exclude = ['status','is_advice','reference', 'user','approval_status','date_created']
        FUNCTION_CHOICES = Band.objects.filter(is_others=False)

        widgets = {
            'ticket_no': forms.TextInput(attrs={'class': 'form-control'}),
            'center_code': forms.TextInput(attrs={'class': 'form-control'}),
            'advance_total_naira': forms.TextInput(attrs={'class': 'form-control', 'required': 'required'}),
            'estimated_cost_naira': forms.TextInput(attrs={'class': 'form-control'}),
            'advance_total_dollar': forms.TextInput(attrs={'class': 'form-control'}),
            'estimated_cost_dollar': forms.TextInput(attrs={'class': 'form-control'}),
            'total_naira': forms.TextInput(attrs={'class': 'form-control'}),
            'total_dollar': forms.TextInput(attrs={'class': 'form-control'}),
            'accomodation_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'accomodation_units': forms.TextInput(attrs={'class': 'form-control'}),
            'flight_rate': forms.TextInput(attrs={'class': 'form-control'}),
            'flight_units': forms.TextInput(attrs={'class': 'form-control'}),
            'approval_level': forms.TextInput(attrs={'class': 'form-control'}),
            'cost_code': forms.TextInput(attrs={'class': 'form-control'}),
            'travel_type': forms.Select(choices=TRAVEL_TYPE, attrs={'class':'form-control'}),
            'trip_type': forms.Select(choices=TRIP_TYPE, attrs={'class': 'form-control'}),
            'function': forms.Select(attrs={'class':'form-control', 'required':'required'}),
            'accommodation_type': forms.Select(choices=ACCOMMODATION_TYPE, attrs={'class':'form-control', 'required':'required'}),
            'purpose':  forms.Select(attrs={'class': 'form-control','required':'required' }),
            'band': forms.Select(attrs={'class': 'form-control', 'required': 'required'}),
            'zone': forms.Select(choices=ZONE, attrs={'class': 'form-control'}),
            'objective': forms.Textarea(attrs={'class': 'form-control', 'required': 'required', 'placeholder': _('Enter travel objective')}),
        }

    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(TravelForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['center_code'].required = False
        self.fields['band'].queryset = Band.objects.filter(is_others=False)



class RoadForm(forms.Form):
    departure_location = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'Required': 'true'}), label=u'Departure location',
        max_length=50, help_text=u'', required=True)
    destination_location = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'Required': 'true'}), label=u'Destination location',
        max_length=50, help_text=u'', required=True)
    mileage = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'Required': 'true'}), label=u'Mileage',
        max_length=50, help_text=u'', required=True)
    departure_date = forms.CharField(widget=forms.TextInput(
        attrs={'type':'date', 'class': 'form-control', 'Required': 'true'}), label=u'Mileage',
        max_length=50, help_text=u'', required=True)

    meal = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Mean Allowance *', 'Required': 'true'}), label=u'Mean allowance days',
        max_length=50, help_text=u'', required=True)


    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('travel_id', None)
        super(RoadForm, self).__init__(*args, **kwargs)