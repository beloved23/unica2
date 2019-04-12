from __future__ import unicode_literals
import collections
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from forms import TravelForm, RoadForm
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from models import *
from datetime import datetime as dt, date
import datetime
import json
from django.core import serializers
from django.conf import settings
from unidecode import unidecode
# Create your views here.
import redis
from newunica.utils import *
from utility.models import Function,Band,Purpose, FunctionalHead
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.core.exceptions import PermissionDenied
import logging


store = redis.Redis(settings.REDIS_SERVER)

class CreateTravel(LoginRequiredMixin, CreateView):
    model = Travel
    form_class = TravelForm
    #def get_form_kwargs(self):
    #    # pass "user" keyword argument with the current user to your form
    #    kwargs = super(CreateTravel, self).get_form_kwargs()
    #    # kwargs['user'] = self.request.user
    #    # kwargs['job'] = get_request_params('pk', **kwargs)
    #    return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        #form.instance.job = Travel.objects.get(pk=self.kwargs['pk'])
        form.save()
        #messages.success(self.request, 'Your ticket id has been created, kindly fill the trip details!')
        return super(CreateTravel, self).form_valid(form)

    def get_success_url(self):
        return reverse('travel:travel_request', args=(self.object.id,))



@csrf_exempt
def createTravelForm(request):
    username = request.user.username
    #result = {u'user': u'20', u'checked': True, u'accommodation_type': u'Hotel', u'zone': u'Zone A', u'groups_len': 1, u'purpose': u'4', u'center_code': u'', u'band': u'2', u'objective': u'hello', u'trip_type': u'Return Flight', u'groups': u'[{"auuid":"2330854","email":"adegokeayanfe","name":"Adegoke Ayanfe"}]', u'travel_type': u'National', u'tfunction': u'11'}
    if request.method == 'POST':
        result = json.loads(request.body.decode('utf-8'))
        try:
            user = User.objects.get(pk=result['user'])
            tfunction = Function.objects.get(pk=result['tfunction'])
            purpose = Purpose.objects.get(pk=result['purpose'])
            band = Band.objects.get(pk=result['band'])
            accommodation_type = result['accommodation_type']
            zone = result['zone']
            center_code = result['center_code']
            objective = result['objective']
            trip_type = result['trip_type']
            travel_type = result['travel_type']
            groups = json.loads(result['groups'])
            group_len = result['groups_len']
            checked = result['checked']
            if checked is None or checked =='':
                checked=False
            res_pk = Travel.objects.create(
                user=user,
                accommodation_type = accommodation_type,
                zone = zone,
                purpose = purpose,
                center_code =center_code,
                band=band,
                objective=objective,
                trip_type=trip_type,
                travel_type = travel_type,
                function=tfunction,
                team_len = int(group_len) + 1,
                is_team = checked
            )
            if checked and group_len > 0:
                for group in groups:
                    TeamTravel.objects.create(travel=res_pk, auuid=group['auuid'], name=group['name'], email=group['email'])
            res = {'action': True, "message": "Travel request created", 'pk': res_pk.pk}
        except Exception, ex:
            logger.error("Error processing rquest %s-%s" % (str(ex), username))
            res = {'action': False, "message": "Travel request created"}
        return HttpResponse(json.dumps(res), content_type='application/json')
    raise PermissionDenied


@csrf_exempt
def aauidValidation(request):
    if request.method == 'POST':
        #print request
        result = request.body.decode('utf-8')
        adResult = json.loads(result)
        username = request.user.username
        auuid = adResult['auuid']
        _res = json.loads(validate_auuid(auuid).decode('utf-8'))
        if _res['FullName'] is None and _res['Email'] is None:
            res = {"isFound": False, "email": "", "name": "", "message": "Invalid auuid or auuid not found!"}
        elif username == auuid:
            res = {"isFound": False, "email": "", "name": '', "message": "Requester's auuid is not allowed!"}
        else:
            res = {"isFound": True, "email": _res['Email'], "name": _res['FullName'], "message": ""}
        return HttpResponse(json.dumps(res), content_type='application/json')
    raise PermissionDenied


class EditTravel(LoginRequiredMixin, UpdateView):
    model = Travel
    template_name_suffix = '_update_form'
    form_class = TravelForm

    def form_valid(self, form):
         messages.success(self.request,
                          'Request successfully updated!')
         self.object = form.save()
         return super(EditTravel, self).form_valid(form)

    def get_success_url(self):
        return reverse('travel:list_travel_request')

    def get_context_data(self, **kwargs):
        context = super(EditTravel, self).get_context_data(**kwargs)
        context['action'] = reverse('travel:edit_travel', kwargs={'pk': self.get_object().id})
        return context


class TravelDetail(LoginRequiredMixin, DetailView):
    model = Travel


@login_required()
def group_all(request, pk):
    obj = get_object_or_404(Travel, pk=pk)
    result = TeamTravel.objects.filter(travel=obj)
    new_data = [ob.as_json() for ob in result]
    return HttpResponse(json.dumps(new_data), content_type='application/json')

def travel_advice(request, pk):
    template = 'flight/travel_advice.html'
    obj = get_object_or_404(Travel, pk=pk)
    context = {'postdetails': pk, 'travel':obj }
    return render(request, template, context)


def testvue(request, template="flight/vuetest.html"):
    return render(request, template)


def travel_json(request):
    data = Travel.objects.filter(user=request.user)
    new_data = [res.json() for res in data]
    #data = serializers.serialize('json', travel)
    return HttpResponse(json.dumps(new_data), content_type='application/json')


def test_date(request):
    template='flight/advice_email.html'
    return render(request, template)


@login_required
def list_travel_request(request, template="flight/broadcast_travel.html"):
    data = Travel.objects.filter(user=request.user).order_by('-date_created')
    context={'username': request.user.username, 'travels': data}
    return render(request, template, context)
    ##travel =Travel.objects.filter(user=request.user)
    #data = serializers.serialize('json', travel)
    #return HttpResponse(json.dumps(data), content_type='application/json')


@login_required
def travel_trip(request, pk):
    template = 'flight/road.html'
    #form = RoadForm(request.POST, travel_id=pk)
    trip_type = get_object_or_404(Travel, pk=pk)
    if trip_type.status=='Completed':
        return redirect('travel:add_travel')
    if trip_type.trip_type == 'Road Trip':
        print 'testing'
        template = 'flight/road.html'
    elif trip_type.trip_type == 'One Way Flight':
        print 'one way'
        template = 'flight/oneway.html'
    elif trip_type.trip_type== 'Multiple Flight':
        print 'multiple'
        template = 'flight/multiple.html'
    elif trip_type.trip_type == 'Return Flight':
        print 'return'
        template = 'flight/return.html'
    purpose = Purpose.objects.all()
    if trip_type.accommodation_type == 'Hotel':
        band = Band.objects.get(name=trip_type.band)
        cost = AccommodationCost.objects.get(band=band, type=trip_type.travel_type, zone=trip_type.zone)
    else:
        band = Band.objects.get(name='Others')
        print '%s-%s-%s' % (band, trip_type.travel_type, trip_type.zone)
        cost = AccommodationCost.objects.get(band=band.pk, type=trip_type.travel_type, zone=trip_type.zone)
    print trip_type
    context = {'postdetails' : pk, 'travel': trip_type, 'accomodation_cost': cost.cost }
    return render(request, template, context)


#class TravelDelete(LoginRequiredMixin, DeleteView):
#    model = Travel
#    #messages.success('Your request was successful')
#    success_url = '/travel/triprequest/'

@login_required
def deleteTravel(request, pk):
    obj = get_object_or_404(Travel, pk=pk)
    obj.delete()
    return redirect('travel:list_travel_request')


def check_work_flow(travel):
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
    return map_list


@login_required
def send_advice(request):
    if request.method == 'POST':
        try:
            result = request.POST
            advice_list = json.loads(result['travel_advice'])
            post_details = result['postdetails']
            travel = get_object_or_404(Travel, id=post_details)
            for res in advice_list:
                TravelAdvice.objects.create(travel=travel, location_name=res['location'], hotel_name=res['hotel'], address=res['address'])
            subject = 'Travel Request | Airtel Travel'
            email_template = 'flight/advice_email.html'
            context_dict = {'host': SITE_URL}
            to = travel.user.email
            from_email = "Airtel Travel <traveldesk@ng.airtel.com>"
            send_email(subject, email_template, [to, ], from_email, context_dict)
            return HttpResponse("<div  class='alert alert-info'>Travel advice sent successfully</div>")
        except Exception, ex:
            print str(ex)
            logger.error(str(ex))
            return HttpResponse("<div class='alert alert-danger'>Your request was unsuccessful! Please contact the site administrator.</div>")
    else:
        return HttpResponse('No found')



@login_required
@transaction.atomic
def road_trip(request):
    if request.method == 'POST':
        try:
            result = request.POST
            departure_location = result['departure_location']
            destination_location = result['destination_location']
            mileage = result['mileage']
            f_type = result['f_type']
            accommodation=result['accommodation']
            totalAdvance = result['totalAdvance']
            totalEstimate = result['totalEstimated']
            accomodation_rate = result['accomodation_rate']
            flight_rate = result['flight_rate']
            flight_units = result['flight_units']
            departure_date = datetime.datetime.strptime(result['departure_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            advance = result['advance']
            post_details = result['postdetails']
            travel=Travel.objects.get(pk=post_details)
            #_road=Road.objects.create(travel=travel, departure_town=departure_location, destination_town=destination_location, mileage=mileage,departure_date=departure_date)
            Trip.objects.create(travel=travel, departure_airport=departure_location, destination_airport=destination_location, departure_date=departure_date,  mileage=mileage)
            accommodation_list = json.loads(accommodation)
            advance_list=json.loads(advance)
            accomodation_days = 0
            for res in accommodation_list:
                name = res['name']
                accomodation_days += int(res['diff'])
                check_in_date = datetime.datetime.strptime(res['check_in_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                check_out_date = datetime.datetime.strptime(res['check_out_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                Accommodation.objects.create(travel=travel, name=name, check_in_date=check_in_date, check_out_date=check_out_date)
            for res in advance_list:
                advance_description = res['advance_description']
                advance = AdvanceDescription.objects.get(name=advance_description)
                units = res['units']
                rate = res['rate']
                cost = res['cost']
                Advance.objects.create(travel=travel, advance_description=advance, units=units, rate=rate, cost=cost)
            travel.status = 'Completed'
            travel.estimated_cost_naira= float(totalEstimate) - float(totalAdvance)
            travel.advance_total_naira=totalAdvance
            travel.total_naira = totalEstimate
            travel.reference = my_random_string(6)
            travel.accomodation_rate = accomodation_rate
            travel.accomodation_units = accomodation_days
            travel.flight_rate = flight_rate
            travel.flight_units = flight_units
            travel.f_type = True if f_type=='true' else False
            travel.date_created = dt.now()
            travel.ticket_no = 'ATD%s' % "{0:05}".format(travel.pk)
            travel.approval_level = check_work_flow(travel)[0]#road_map_list[0] #line manager is always the first to approve
            travel.save()
            # call function
            workflow_trip_mapping(request.user, travel.reference, 0)
        # #look up who will be in charge of the request and process mail
        # subject = 'Travel Request | Airtel Travel'
        # email_template = 'flight/approval-request.html'
        # to = request.user.email #change this part to the conrresponding email (e.g: line manager email)
        # from_email = "Airtel Travel <hello@airtel.ng>"
        # context_dict = {'travel': travel, 'user': request.user, 'host': request.META['HTTP_HOST']}
        # send_email(subject, email_template, [to, ], from_email, context_dict)
        # #messages.success(request, 'Your request has been logged! Please check your email for update on approval')
        # #logger.debug(request.POST)
        # #return HttpResponseRedirect(reverse('home'))
            return HttpResponse("<div  class='alert alert-info'>Your request has been logged! Please check your email for update on approval</div>")
        except ApprovalMapping.DoesNotExist:
             logger.info('Approval Mapping does not exit for %s' % request.user)
             return HttpResponse("<div class='alert alert-danger'>Your request was unsuccessful! Please contact the site administrator.</div>")
        except Exception, ex:
             logger.info('%s-%s' % (str(ex), request.user))
             return HttpResponse("<div class='alert alert-danger'>Your request was unsuccessful! Please contact the site administrator.</div>")
    else:
        return HttpResponse('Access Denied')


@login_required
@transaction.atomic
def one_way_trip(request):
    #import pdb
    #pdb.set_trace()
    if request.method == 'POST':
        try:
            result = request.POST
            totalEstimatedDollar = result['totalEstimatedDollar']
            totalEstimatedNaira = result['totalEstimatedNaira']
            totalAdvanceDollar = result['totalAdvanceDollar']
            totalAdvanceNaira = result ['totalAdvanceNaira']
            departure_location = result['departure_location']
            destination_location = result['destination_location']
            flight_cost = result['flight_cost']
            f_type = result['f_type']
            accomodation_rate = result['accomodation_rate']
            flight_rate = result['flight_rate']
            flight_units = result['flight_units']
            departure_date = datetime.datetime.strptime(result['departure_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            #arrival_date = datetime.datetime.strptime(result['departure_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            advance = result['advance']
            accommodation = result['accommodation']
            post_details = result['postdetails']
            travel=Travel.objects.get(pk=post_details)
            Trip.objects.create(travel=travel, departure_airport=departure_location, destination_airport=destination_location, departure_date=departure_date,  flight_cost=flight_cost)
            accommodation_list = json.loads(accommodation)
            advance_list = json.loads(advance)
            accomodation_days = 0
            for res in accommodation_list:
                name = res['name']
                accomodation_days += int(res['diff'])
                check_in_date = datetime.datetime.strptime(res['check_in_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                check_out_date = datetime.datetime.strptime(res['check_out_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                Accommodation.objects.create(travel=travel, name=name, check_in_date=check_in_date,
                                                check_out_date=check_out_date)
            for res in advance_list:
                advance_description = res['advance_description']
                advance = AdvanceDescription.objects.get(name=advance_description)
                units = res['units']
                rate = res['rate']
                cost = res['cost']
                currency= res['currency']
                Advance.objects.create(travel=travel, advance_description=advance, units=units, rate=rate,currency=currency, cost=cost)
            travel.estimated_cost_naira = float(totalEstimatedNaira) - float(totalAdvanceNaira)
            travel.advance_total_naira = totalAdvanceNaira
            travel.advance_total_dollar = totalAdvanceDollar
            travel.estimated_cost_dollar = float(totalEstimatedDollar) - float(totalAdvanceDollar)
            travel.total_naira = totalEstimatedNaira
            travel.total_dollar = totalEstimatedDollar
            travel.accomodation_rate = accomodation_rate
            travel.accomodation_units = accomodation_days
            travel.flight_rate = flight_rate
            travel.f_type = True if f_type=='true' else False
            travel.flight_units = flight_units
            travel.reference = my_random_string(6)
            travel.ticket_no = 'ATD%s' % "{0:05}".format(travel.pk)
            travel.approval_level = check_work_flow(travel)[0]  #check_work_flow(travel)[0]
            travel.status = 'Completed'
            travel.date_created = dt.now()
            travel.save()
            #call workflow function
            workflow_trip_mapping(request.user, travel.reference, 0)
            #messages.success(request, 'Your request has been logged! Please check your email for update on approval')
            #logger.debug(request.POST)
            #return HttpResponseRedirect(reverse('home'))
            logger.info('sent respnse back')
            return HttpResponse("<div  class='alert alert-info'>Your request has been logged! Please check your email for update on approval</div>")
        except ApprovalMapping.DoesNotExist:
             logger.info('Approval Mapping does not exit for %s' % request.user)
             return HttpResponse("<div class='alert alert-danger'>Your request was unsuccessful! Please contact the site administrator.</div>")
        except Exception, ex:
             logger.info('%s - %s' % (str(ex), request.user))
             return HttpResponse("<div class='alert alert-danger'>Your request was unsuccessful! Please contact the site administrator.</div>")
    else:
        return HttpResponse('Access Denied')


@login_required
@transaction.atomic
def return_flight_trip(request):
    if request.method=='POST':
        try:
            result = request.POST
            departure_location = result['departure_location']
            destination_location = result['destination_location']
            totalEstimatedDollar= result['totalEstimatedDollar']
            totalEstimatedNaira= result['totalEstimatedNaira']
            totalAdvanceDollar= result['totalAdvanceDollar']
            totalAdvanceNaira= result['totalAdvanceNaira']
            flight_cost = result['flight_cost']
            f_type = result['f_type']
            accomodation_rate = result['accomodation_rate']
            flight_rate = result['flight_rate']
            flight_units = result['flight_units']
            departure_date = datetime.datetime.strptime(result['departure_date'], '%m/%d/%Y').strftime('%Y-%m-%d') #result['departure_date'] datetime.datetime.strptime(result['departure_date'], '%Y-%m-%d').strftime('%Y-%m-%d')
            #arrival_date = datetime.datetime.strptime(result['departure_date'], '%m/%d/%Y').strftime('%Y-%m-%d')#result['departure_date'] datetime.datetime.strptime(result['departure_date'], '%Y-%m-%d').strftime('%Y-%m-%d')
            return_departure_date =datetime.datetime.strptime(result['return_departure_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            #return_arrival_date = datetime.datetime.strptime(result['return_arrival_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
            advance = result['advance']
            accommodation = result['accommodation']
            post_details = result['postdetails']
            travel=Travel.objects.get(pk=post_details)
            accommodation_list = json.loads(accommodation)
            advance_list = json.loads(advance)
            accomodation_days = 0
            Trip.objects.create(travel=travel, departure_airport=departure_location, destination_airport= destination_location, departure_date=departure_date, flight_cost=flight_cost)
            Trip.objects.create(travel=travel, departure_airport=destination_location, destination_airport= departure_location, departure_date=return_departure_date, is_return=True)
            for res in accommodation_list:
                name = res['name']
                accomodation_days += int(res['diff'])
                check_in_date = datetime.datetime.strptime(res['check_in_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                check_out_date = datetime.datetime.strptime(res['check_out_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                Accommodation.objects.create(travel=travel, name=name, check_in_date=check_in_date,
                                                check_out_date=check_out_date)
            for res in advance_list:
                advance_description = res['advance_description']
                advance = AdvanceDescription.objects.get(name=advance_description)
                units = res['units']
                rate = res['rate']
                cost = res['cost']
                currency = res['currency']
                Advance.objects.create(travel=travel, advance_description=advance, units=units, rate=rate,
                                        currency=currency, cost=cost)
            travel.estimated_cost_naira = float(totalEstimatedNaira) - float(totalAdvanceNaira)
            travel.advance_total_naira = totalAdvanceNaira
            travel.advance_total_dollar = totalAdvanceDollar
            travel.estimated_cost_dollar = float(totalEstimatedDollar) - float(totalAdvanceDollar)
            travel.total_naira = totalEstimatedNaira
            travel.total_dollar = totalEstimatedDollar
            travel.accomodation_rate = accomodation_rate
            travel.accomodation_units = accomodation_days
            travel.flight_rate = flight_rate
            travel.flight_units = flight_units
            travel.f_type = True if f_type=='true' else False
            travel.status = 'Completed'
            travel.ticket_no = 'ATD%s' % "{0:05}".format(travel.pk)
            travel.reference = my_random_string(6)
            travel.date_created = dt.now()
            travel.approval_level = check_work_flow(travel)[0]
            travel.save()
            #Call workflow function
            workflow_trip_mapping(request.user, travel.reference, 0)
            #messages.success(request, 'Your request has been logged! Please check your email for update on approval')
            #logger.debug(request.POST)
            #return HttpResponseRedirect(reverse('home'))
            return HttpResponse("<div  class='alert alert-info'>Your request has been logged! Please check your email for update on approval</div>")
            # except ApprovalMapping.DoesNotExist:
            #     logger.info('Approval Mapping does not exit for %s' % request.user)
            #     return HttpResponse("<div class='alert alert-danger'>Your request was unsuccessful! Please contact the site administrator.</div>")
            # except Exception, ex:
            #     logger.info('%s - %s' % (str(ex), request.user))
            #     return HttpResponse("<div class='alert alert-danger'>Your request was unsuccessful! Please contact the site administrator.</div>")
        except ApprovalMapping.DoesNotExist:
            logger.info('Approval Mapping does not exit for %s' % request.user)
            return HttpResponse("<div class='alert alert-danger'>Your request was unsuccessful! Please contact the site administrator.</div>")
        except Exception, ex:
            logger.info('%s - %s' % (str(ex), request.user))
            return HttpResponse("<div class='alert alert-danger'>Your request was unsuccessful! Please contact the site administrator.</div>")
    return HttpResponse('Access Denied')



@login_required
@transaction.atomic
def multiple_flight_trip(request):
    if request.method == 'POST':
        try:
            result = request.POST
            flights = result['flight']
            totalEstimatedDollar = result['totalEstimatedDollar']
            totalEstimatedNaira = result['totalEstimatedNaira']
            totalAdvanceDollar = result['totalAdvanceDollar']
            totalAdvanceNaira = result['totalAdvanceNaira']
            accomodation_rate = result['accomodation_rate']
            f_type = result['f_type']
            flight_rate = result['flight_rate']
            flight_units = result['flight_units']
            #flight_len = result['flight_len']
            #departure_date = result['departure_date'] #datetime.datetime.strptime(result['departure_date'], '%Y-%m-%d').strftime('%Y-%m-%d')
            #arrival_date = result['departure_date'] #datetime.datetime.strptime(result['departure_date'], '%Y-%m-%d').strftime('%Y-%m-%d')
            #return_departure_date = result['return_departure_date']
            #return_arrival_date = result['return_arrival_date']
            advance = result['advance']
            accommodation = result['accommodation']
            post_details = result['postdetails']
            flights_list = json.loads(flights)
            accommodation_list = json.loads(accommodation)
            advance_list = json.loads(advance)
            travel = Travel.objects.get(pk=post_details)
            accomodation_days = 0
            for flight in flights_list:
                departure_date = datetime.datetime.strptime(flight['departure_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                #arrival_date = datetime.datetime.strptime(flight['arrival_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                Trip.objects.create(travel=travel, departure_airport=flight['departure_airport'],
                                        destination_airport=flight['destination_airport'], departure_date=departure_date,
                                        flight_cost=flight['flight_cost'])
            for res in accommodation_list:
                name = res['name']
                accomodation_days += int(res['diff'])
                check_in_date = datetime.datetime.strptime(res['check_in_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                check_out_date = datetime.datetime.strptime(res['check_out_date'], '%m/%d/%Y').strftime('%Y-%m-%d')
                Accommodation.objects.create(travel=travel, name=name, check_in_date=check_in_date,
                                                check_out_date=check_out_date)
            for res in advance_list:
                advance_description = res['advance_description']
                advance = AdvanceDescription.objects.get(name=advance_description)
                units = res['units']
                rate = res['rate']
                cost = res['cost']
                currency = res['currency']
                Advance.objects.create(travel=travel, advance_description=advance, units=units, rate=rate,
                                        currency=currency, cost=cost)
            travel.reference = my_random_string(6)
            travel.estimated_cost_naira = float(totalEstimatedNaira) - float(totalAdvanceNaira)
            travel.advance_total_naira = totalAdvanceNaira
            travel.advance_total_dollar = totalAdvanceDollar
            travel.estimated_cost_dollar = float(totalEstimatedDollar) - float(totalAdvanceDollar)
            travel.total_naira = totalEstimatedNaira
            travel.total_dollar = totalEstimatedDollar
            travel.accomodation_rate = accomodation_rate
            travel.accomodation_units = accomodation_days
            travel.flight_rate = flight_rate
            travel.flight_units = flight_units
            travel.f_type = True if f_type=='true' else False
            travel.ticket_no = 'ATD%s' % "{0:05}".format(travel.pk)
            travel.status = 'Completed'
            travel.date_created = dt.now()
            travel.approval_level = check_work_flow(travel)[0]
            travel.save()
            #call workflow function
            workflow_trip_mapping(request.user, travel.reference, 0)
            #messages.success(request, 'Your request has been logged! Please check your email for update on approval')
            #logger.debug(request.POST)
            #return HttpResponseRedirect(reverse('home'))
            return HttpResponse("<div  class='alert alert-info'>Your request has been logged! Please check your email for update on approval</div>")
        except ApprovalMapping.DoesNotExist:
             logger.info('Approval Mapping does not exit for %s' % request.user)
             return HttpResponse("<div class='alert alert-danger'>Your request was unsuccessful! Please contact the site administrator.</div>")
        except Exception, ex:
             logger.info('%s - %s' % (str(ex), request.user))
             return HttpResponse("<div class='alert alert-danger'>Your request was unsuccessful! Please contact the site administrator.</div>")
    else:
        return HttpResponse('Access Denied')


@login_required

def test(request):
    template = 'flight/oneway.html'
    context = { 'username': request.user}
    return render(request, template, context)


@login_required
def approve(request, template='flight/approval/approve-travel.html'):
    reference = request.GET.get('reference')
    approval_level = request.GET.get('approval')
    try:
        #import pdb
        #pdb.set_trace()
        travel_obj = Travel.objects.get(reference=reference)
        standing_approval = Approvals.objects.get(reference=reference)
        user_obj = travel_obj.user
        #update travel and send user an email of approval, then get next approval and send an email as well
        #do next person update and search for corresponding I.E: search for corrensponding person
        #check the type of travel and call corresponding list
        map_list = []
        #if travel_obj.trip_type == 'Road Trip':
        #    map_list = road_map_list
        num_results = FunctionalHead.objects.filter(name=travel_obj.user).count()
        if num_results >= 1:
            map_list = ec_map_list
        elif travel_obj.purpose == 'Training':
            map_list = training_map_list
        elif travel_obj.trip_type == 'Road Trip':
            map_list = road_map_list
        elif travel_obj.travel_type == 'National':
            map_list = national_map_list
        elif travel_obj.travel_type == 'International':
            map_list = international_map_list

        next_person_index = map_list.index(approval_level)
        next_person_index += 1
        message = ('You have successfully approved the travel request for %s %s with auuid %s' % (travel_obj.user.first_name, travel_obj.user.last_name,  travel_obj.user.username))
        context = {'travel': travel_obj, 'message':message, 'tag':'success'}
        workflow_trip_mapping(request.user, travel_obj.reference, 1)
        standing_approval.is_approved = True
        standing_approval.status='COMPLETED'
        standing_approval.save()
        # approval_mapping = ApprovalMapping.objects.get(employee=user_obj)
        #oya send mail to the next person
        # try:
        #     subject = 'Travel Request | Airtel Travel'
        #     email_template = 'flight/approval-request.html'
        #     to = map_list[next_person_index]  # change this part to the conrresponding email (e.g: line manager email)
        #     from_email = "Airtel Travel <hello@airtel.ng>"
        #     context_dict = {'travel': travel_obj, 'user': request.user, 'host': request.META['HTTP_HOST']}
        #     send_email(subject, email_template, [to, ], from_email, context_dict)
        # except IndexError: #list has gotten to an end, mail user
        #     subject = 'Travel Request | Airtel Travel'
        #     email_template = 'flight/acceptance.html'
        #     to = travel_obj.user.email  # change this part to the conrresponding email (e.g: line manager email)
        #     from_email = "Airtel Travel <hello@airtel.ng>"
        #     context_dict = {'travel': travel_obj, 'user': request.user, 'host': request.META['HTTP_HOST']}
        #     send_email(subject, email_template, [to, ], from_email, context_dict)
        return render(request, template, context)
    except Travel.DoesNotExist:
        check_if_approved = store.sismember(settings.APPROVAL_KEY, reference)
        logger.info('%s-%s' % (check_if_approved, reference))
        if check_if_approved:
            message = 'Your decision has already been appropriated for this travel request'
        else:
            message = 'There is no request with this reference'
        context = {'message': message, 'tag':'danger'}
        return render(request, template, context)
    except Exception, ex:
        logger.info('An error occured %s' % str(ex))
        message = "An error occured! please try again"
        context = {'message': message, 'tag':'danger'}
        return render(request, template, context)


def approval_check(reference, subject, email):
    try:
        travel_obj = Travel.objects.get(reference=reference)
        standing_approval = Approvals.objects.get(reference=reference)
        user_obj = travel_obj.user
        #update travel and send user an email of approval, then get next approval and send an email as well
        #do next person update and search for corresponding I.E: search for corrensponding person
        #check the type of travel and call corresponding list
        map_list = []
        #if travel_obj.trip_type == 'Road Trip':
        #    map_list = road_map_list
        if standing_approval.approval_person_email == email:
            num_results = FunctionalHead.objects.filter(name=travel_obj.user).count()
            if num_results >= 1:
                map_list = ec_map_list
            elif travel_obj.purpose == 'Training':
                map_list = training_map_list
            elif travel_obj.trip_type == 'Road Trip':
                map_list = road_map_list
            elif travel_obj.travel_type == 'National':
                map_list = national_map_list
            elif travel_obj.travel_type == 'International':
                map_list = international_map_list
            next_person_index = map_list.index(travel_obj.approval_level)
            next_person_index += 1
            message = ('You have successfully approved the travel request for %s %s with reference no.  %s' % (travel_obj.user.first_name, travel_obj.user.last_name, reference))
            #context = {'travel': travel_obj, 'message':message, 'tag':'success'}
            context = "You have successfully approved the travel request"
            logger.info("You have successfully approved the travel request %s "  % reference)
            workflow_trip_mapping(travel_obj.user, travel_obj.reference, 1)
            send_reply(reference, message, subject)
            standing_approval.is_approved = True
            standing_approval.status='COMPLETED'
            standing_approval.save()
            return context
        else:
            message = "You have no pending approval."
            send_reply_invalid(email, message, subject)
    except Travel.DoesNotExist:
        check_if_approved = store.sismember(settings.APPROVAL_KEY, reference)
        logger.info('%s-%s' % (check_if_approved, reference))
        if check_if_approved:
            message = 'Your decision has already been appropriated  for this travel request'
        else:
            message = 'There is no request with this reference'
        send_reply(reference, message, subject)
        #context = {'message': message, 'tag':'danger'}
    except Exception, ex:
        logger.info('An error occured %s' % str(ex))
        message = "An error occured! please try again"
        #context = {'message': message, 'tag':'danger'}
    return message


def send_reply(reference, message, subject):
    #subject = 'Travel Request | Airtel Travel'
    email_template = 'flight/approval/acknowledge.html'
    #to = user_obj.email  # leave this part because its the user that will receive the email
    from_email = "Airtel Travel <travel@ng.airtel.ng>"
    approval = Approvals.objects.get(reference=reference)
    to = approval.approval_person_email
    context_dict = {'name': approval.approval_person_name, 'message': message}
    send_email(subject, email_template, [to, ], from_email, context_dict)


def send_reply_invalid(email, message, subject):
    subject = 'Travel Request | Airtel Travel'
    email_template = 'flight/approval/acknowledge.html'
    from_email = "Airtel Travel <travel@ng.airtel.ng>"
    context_dict = {'message': message}
    send_email(subject, email_template, [email, ], from_email, context_dict)


def reject(request, template='flight/approval/reject-travel.html'):
    reference = request.GET.get('reference')
    approval_level = request.GET.get('approval')
    context = {}
    try:
        travel_obj = Travel.objects.get(reference=reference)
        standing_approval = Approvals.objects.get(reference=reference)
        user_obj = travel_obj.user
        map_list = []
        store.sadd(settings.APPROVAL_KEY, reference)
        if travel_obj.trip_type == 'Road Trip':
            map_list = road_map_list
        #update travel and send user an email of reject
        travel_obj.approval_level = standing_approval.approval_person_level
        # update reference always, so one person cannot reject twice or so
        travel_obj.approval_status = "Rejected"
        travel_obj.reference = my_random_string(6)
        travel_obj.save()
        #context['travel'] = travel_obj
        #oya send mail to the next person
        #import pdb
        #pdb.set_trace()
        subject = 'Travel Request Rejected | Airtel Travel'
        email_template = 'flight/approval/rejection.html'
        to = user_obj.email  # leave this part because its the user that will receive the email
        from_email = "Airtel Travel <hello@airtel.ng>"
        message = "You have rejected the travel request for %s %s with reference no. %s" % (travel_obj.user.first_name, travel_obj.user.last_name, reference)
        context = {'travel': travel_obj, 'message': message, 'user': request.user, 'host': request.META['HTTP_HOST'], 'tag':'danger'}
        send_email(subject, email_template, [to, ], from_email, context)
        standing_approval.is_approved = False
        standing_approval.status='COMPLETED'
        standing_approval.save()
        return render(request, template, context)
    except Travel.DoesNotExist:
        check_if_rejected = store.sismember(settings.APPROVAL_KEY, reference)
        logger.info('%s-%s' % (check_if_rejected, reference))
        if check_if_rejected:
            message = 'Your decision has already been appropriated  for this travel request with reference no %s' % reference
        else:
            message = 'There is no request with this reference'
        context = {'message': message, 'tag':'danger'}
        return render(request, template, context)
    except Exception, ex:
        logger.info('An error occured %s' % str(ex))
        message = "An error occured! please try again"
        context = {'message': message, 'tag':'danger'}
        return render(request, template, context)


def reject_check(reference, subject, email):
    try:
        travel_obj = Travel.objects.get(reference=reference)
        standing_approval = Approvals.objects.get(reference=reference)
        user_obj = travel_obj.user
        map_list = []
        store.sadd(settings.APPROVAL_KEY, reference)

        if standing_approval.approval_person_email == email:
            if travel_obj.trip_type == 'Road Trip':
                map_list = road_map_list
            #update travel and send user an email of reject
            #travel_obj.approval_level = approval_level
            # update reference always, so one person cannot reject twice or so
            travel_obj.reference = my_random_string(6)
            #context['travel'] = travel_obj
            #oya send mail to the next person
            subject_reject = 'Travel Request Rejected | Airtel Travel'
            email_template = 'flight/approval/rejection.html'
            to = user_obj.email  # leave this part because its the user that will receive the email
            from_email = "Airtel Travel <travel@ng.airtel.com>"
            context_dict = {'travel': travel_obj, 'user': user_obj}
            send_email(subject_reject, email_template, [to, ], from_email, context_dict)
            message = "You have rejected the travel request for %s %s with reference no. %s" % (travel_obj.user.first_name, travel_obj.user.last_name, reference)
            standing_approval.is_approved = False
            standing_approval.status='COMPLETED'
            standing_approval.save()
            send_reply(reference, message, subject)
            travel_obj.approval_status = 'Rejected'
            travel_obj.save()
            #return  context_dict
        else:
            message = "You have no pending request"
            send_reply_invalid(email, message, subject)
    except Travel.DoesNotExist:
        check_if_rejected = store.sismember(settings.APPROVAL_KEY, reference)
        logger.info('%s-%s' % (check_if_rejected, reference))
        if check_if_rejected:
            message = 'Your decision has already been appropriated for this travel request with reference no. %s' % reference
        else:
            message = 'There is no request with this reference'
        context = {'message': message, 'tag':'danger'}
        send_reply(reference, message, subject)
        #return context
    except Exception, ex:
        logger.info('An error occured %s' % str(ex))
        message = "An error occured! please try again"
        #context = {'message': message, 'tag':'danger'}
        #return context
    return message


@login_required
def download_file(request):
    logger.info('New Request....')
    try:
        mime = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        filename='travelpolicy.pdf'
        fpath= os.path.join(settings.TRAVEL_POLICY, 'travelpolicy.pdf')
        print fpath
        _file = open(fpath, 'rb')
        response = HttpResponse(_file.read(), content_type='application/pdf')
        # response['content_type'] = 'application/pdf'
        response['Content-Disposition'] = 'attachment;filename=%s' % filename  # % filename
        return response
    except Exception, ex:
        logger.info('An error occured %s' % str(ex))
        return HttpResponse('An Error occured!, please try again later')




@csrf_exempt
def email_approval(request):
    response= {'Status':0, 'Message': 'Invallid request mess'}
    # import pdb
    # pdb.set_trace()
    if request.method == 'POST':
        try:
            logger.info('Update approval')
            logger.info('log request %s' % request.body)
            obj = json.loads(request.body)
            subject = obj['subject'].split('::')
            email = obj['sender']
            email_spl = email.split('@')
            if email_spl[1] != "ng.airtel.com":
                subject_reject = 'Travel Request | Airtel Travel'
                email_template = 'flight/approval/no-email.html'
                to = email
                from_email = "Airtel Travel <travel@ng.airtel.com>"
                context_dict = {}
                response = {'Status': False, 'Message': 'Invalid email'}
                send_email(subject_reject, email_template, [to, ], from_email, context_dict)
            else:
                if subject[2] == "Approved":
                    res = approval_check(subject[1], obj['subject'], email)
                elif subject[2] == "Rejected":
                    res = reject_check(subject[1], obj['subject'], email)
                response = {'Status': True, 'Message': res}
        except Exception, ex:
            logger.info('An error occured %s' % str(ex))
            response = {'Status': False, 'Message': 'Failed'}
    else:
        response = {'Status': '2', 'Message': 'Invalid method'}
    return HttpResponse(json.dumps(response), content_type='application/json')

