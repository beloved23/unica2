from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^broadcast/$', CreateBroadcast.as_view(), {}, name='add_broadcast'),
    url(r'^upload/$', CreateUploads.as_view(), {}, name='upload_list'),
    # url(r'^create/(?P<pk>\d+)$', travel_trip, name='travel_request'),
    # url(r'^traveladvice/(?P<pk>\d+)$', travel_advice, name='travel_advice'),
    url(r'^import/$', import_report , name='import_report'),
    url(r'^listbroadcast/$', BroadList.as_view() , name='broad_list'),
    url(r'^target/$', createBroadcast, name='target'),
    url(r'^targetupload/$', upload, name='targetupload'),
]