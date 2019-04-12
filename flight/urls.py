from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^add/$', CreateTravel.as_view(), {}, name='add_travel'),
    url(r'^vue/$', testvue, {}, name='vue_travel'),
    url(r'^create/(?P<pk>\d+)$', travel_trip, name='travel_request'),
    url(r'^traveladvice/(?P<pk>\d+)$', travel_advice, name='travel_advice'),
    url(r'^advice/$', send_advice , name='send_advice'),
    url(r'^emails/$', aauidValidation , name='email_advice'),
    url(r'^ticket/$', createTravelForm, name='travel_form'),
    url(r'^roadadd/$', road_trip, name='travel_road'),
    url(r'^onewaytrip/$', one_way_trip, name='travel_one_way_trip'),
    url(r'^returntrip/$', return_flight_trip , name='travel_return_flight_trip'),
    url(r'^multipletrip/$', multiple_flight_trip , name='travel_return_flight_trip'),
    url(r'^travaljson/$', travel_json, name='travel_test'),
    url(r'^triprequest/$', list_travel_request, name='list_travel_request'),
    url(r'^policy/$', download_file, name='travel_request_policy'),
    url(r'^test/$', test_date, name='travel_request_date'),
    url(r'^edit/(?P<pk>\d+)/$', EditTravel.as_view(), name='edit_travel'),
    url(r'^(?P<pk>\d+)/$', TravelDetail.as_view(), name='travel_detail'),
    #url(r'^flight/delete/(?P<pk>\d+)$', TravelDelete.as_view(), name='delete'),
    url(r'^delete/(?P<pk>\d+)$', deleteTravel, name='travel_delete'),
    url(r'^api/email_approval/$', email_approval, name='email_approval'),
    url(r'^group/(?P<pk>\d+)$', group_all, name='travel_group'),

]

