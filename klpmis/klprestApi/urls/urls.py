from django.conf.urls.defaults import patterns, url
from klprestApi.views.AllidsActivate import KLP_Activation, KLP_act_form

urlpatterns = patterns('', url(r'^KLP_activaterecords/$',
                       KLP_Activation),
                       url(r'^KLP_activaterecords_form/$',
                       KLP_act_form))
