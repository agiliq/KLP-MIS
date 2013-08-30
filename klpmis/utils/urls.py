from django.conf.urls import patterns, url

from .views import KLP_Set_Session
from klprestApi.HomeApi import KLP_Home

urlpatterns = patterns('',
    url(r'^home/$', KLP_Home(permitted_methods=('GET',)), name='home'),
    url(r'^set/session/$', KLP_Set_Session)
)
