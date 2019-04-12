from django.conf.urls import url
from account.views import *

urlpatterns = [
    url(r'^$', dashboard, {}, name='home'),
    url(r'^login/$', LoginView.as_view(), {}, name='login'),
    url(r'^logout/$', logout, {}, name='logout'),
]