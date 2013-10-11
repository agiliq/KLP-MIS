from django.conf.urls import patterns, url

from klprestApi.views.AllidsActivate import KLP_Activation, KLP_act_form
from klprestApi.views.AnswerApi import \
    KLP_DataEnry, KLP_DataValidation, KLP_getAnswers
from klprestApi.views.AssessmentApi import \
    AssessmentView, AssessmentCreate, AssessmentLookupCreate,\
    AssessmentLookupCopy, AssessmentLookupList, AssessmentLookupMultieditor,\
    AssessmentUpdate, KLP_Assessment_Lookup_Update, KLP_Get_Assessments, \
    KLP_copy_Assessments, KLP_lookup_inlineEdit
from klprestApi.views.BoundryApi import KLP_Boundary_View,\
    KLP_Boundary_Create, KLP_Boundary_Update
from klprestApi.views.BoundaryTypeApi import \
    template_boundary_type_view
from klprestApi.views.ChildApi import KLP_Child_Create,\
    KLP_Child_View, KLP_Child_Update, childsql, ChildrenList, StdGrpFilter


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
                       url(r'^assessment_lookup_value/inlineedit/?$', KLP_lookup_inlineEdit),
                       url(r'^boundary/(?P<boundary_id>\d+)/(?P<boundarytype_id>\d+)/view/$', KLP_Boundary_View),
                       url(r'^boundary/creator/?$', KLP_Boundary_Create),
                       url(r'^boundary/(?P<boundary_id>\d+)/update/$', KLP_Boundary_Update),
                       url(r'^boundary-type/creator/?$',
                           template_boundary_type_view.responder.create_form,
                       {'form_class': 'boundary_type'}),
                       url(r'^boundary/(?P<referKey>.*)/child/creator/$',
                           KLP_Child_Create),
                       url(r'^child/(?P<child_id>\d+)/view/?$', KLP_Child_View),
                       url(r'^child/(?P<child_id>\d+)/update/?$', KLP_Child_Update),
                       url(r'^boundary/(?P<boundary_id>\d+)/child/view/$', ChildrenList),
                       url(r'^filter/(?P<school_id>\d+)/schgrp/$',
                           StdGrpFilter(permitted_methods=('POST', 'GET'))),
                       url(r'^childsql/(?P<boundary_id>\d+)/$', childsql),)
