from django.conf.urls.defaults import patterns, url

from klprestApi.views.AllidsActivate import KLP_Activation, KLP_act_form
from klprestApi.views.AnswersApi import KLP_DataEnry, KLP_DataValidation, KLP_getAnswers

urlpatterns = patterns('', url(r'^KLP_activaterecords/$',
                       KLP_Activation),
                       url(r'^KLP_activaterecords_form/$',
                       KLP_act_form),
                       url(r'^answer/data/entry/$', KLP_DataEnry),
                       url(r'^answer/data/validation/$', KLP_DataValidation),
                       url(r'^klp/getanswers/$', KLP_getAnswers))
