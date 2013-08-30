from django.conf.urls import patterns, url

from .views import set_session
from klprestApi.HomeApi import KLP_Home

urlpatterns = patterns('',
    url(r'^home/$', KLP_Home(), name='home'),
    url(r'^set/session/$', set_session, name='set_session')
)
