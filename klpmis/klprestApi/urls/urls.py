from django.conf.urls.defaults import patterns, url

from klprestApi.views.AllidsActivate import KLP_Activation, KLP_act_form
from klprestApi.views.AnswerApi import \
    KLP_DataEnry, KLP_DataValidation, KLP_getAnswers
from klprestApi.views.AssessmentApi import AssessmentView, AssessmentCreate, AssessmentLookupCreate, AssessmentLookupCopy, \
    AssessmentLookupList, AssessmentLookupMultieditor, AssessmentUpdate, \
    KLP_Assessment_Lookup_Update, KLP_Get_Assessments, KLP_copy_Assessments,\
    KLP_lookup_inlineEdit


urlpatterns = patterns('', url(r'^KLP_activaterecords/$', KLP_Activation),
                       url(r'^KLP_activaterecords_form/$', KLP_act_form),
                       url(r'^answer/data/entry/$', KLP_DataEnry),
                       url(r'^answer/data/validation/$', KLP_DataValidation),
                       url(r'^klp/getanswers/$', KLP_getAnswers),
                       url(r'^assessment/(?P<assessment_id>\d+)/view/?$',
                           AssessmentView),
                       url(r'^programme/assessment/(?P<referKey>\d+)/creator/?$',
                           AssessmentCreate),
                       url(r'^programme/assessment/assessment_lookup/(?P<referKey>\d+)/creator/?$',
                           AssessmentLookupCreate),
                       url(r'^assessment/assessment_lookup/(?P<referKey>\d+)/copy/?$',
                           AssessmentLookupCopy),
                       url(r'^assessment/assessment_lookup/(?P<referKey>\d+)/view/?$',
                           AssessmentLookupList),
                       url(r'^assessment/assessment_lookup/(?P<assessment_id>\d+)/multieditor/?$',
                           AssessmentLookupMultieditor),
                       url(r'^assessment/(?P<assessment_id>\d+)/update/?$',
                           AssessmentUpdate),
                       url(r'^assessment/(?P<referKey>\d+)/assessment_lookup/(?P<assessment_lookup_id>\d+)/update/?$',
                           KLP_Assessment_Lookup_Update),
                       url(r'^assessment/(?P<referKey>\d+)/assessment_lookup/(?P<assessment_lookup_id>\d+)/update/(?P<counter>\d+)/?$',
                           KLP_Assessment_Lookup_Update),
                       url(r'^filter/programme/(?P<programme_id>\d+)/assessments/$',
                           KLP_Get_Assessments(permitted_methods=('POST', 'GET'))),
                       url(r'^assessment/(?P<assessment_id>\d+)/copy/?$',
                           KLP_copy_Assessments),
                       url(r'^assessment_lookup_value/inlineedit/?$', KLP_lookup_inlineEdit),)