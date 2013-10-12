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
from klprestApi.views.ConsoleApi import KLP_Admin_Console, KLP_Run_Query
from klprestApi.views.InstitutionApi import KLP_Institution_Create,\
    KLP_Institution_View, KLP_Institution_Update, KLP_Institution_Boundary
from klprestApi.views.InstitutionCategoryApi import\
    KLP_Institution_Category_Create
from klprestApi.views.InstitutionManagementApi import\
    KLP_Institution_Management_Create
from klprestApi.views.KLP_AuditTrial import KLP_audit
from klprestApi.views.KLP_Common import KLP_Create_Node, KLP_Delete,\
    KLP_flogin, KLP_glogin
from klprestApi.views.KLP_Map import KLP_Map_SG
from klprestApi.views.KLP_Permission import KLP_Assign_Permissions,\
    KLP_Users_list, KLP_User_Delete, KLP_User_Activate,\
    KLP_User_Permissions, KLP_Show_Permissions, KLP_Revoke_Permissions,\
    KLP_ReAssign_Permissions, KLP_Show_User_Permissions
from klprestApi.views.LanguageApi import KLP_Language_Create
from klprestApi.views.ProgrammeApi import KLP_Programme_View,\
    KLP_Programme_Create, KLP_Programme_Update, KLP_Get_Programms


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
                       url(r'^childsql/(?P<boundary_id>\d+)/$', childsql),
                       url(r'^console/?$', KLP_Admin_Console),
                       url(r'^run-query/?$', KLP_Run_Query),
                       url(r'^boundary/(?P<referKey>\d+)/institution/creator/$',
                           KLP_Institution_Create),
                       url(r'^institution/(?P<institution_id>\d+)/view/?$',
                           KLP_Institution_View),
                       url(r'^institution/(?P<institution_id>\d+)/update/?$',
                           KLP_Institution_Update),
                       url(r'^boundary/(?P<boundary_id>\d+)/(?P<permissionType>\w+)/?$',
                           KLP_Institution_Boundary),
                       url(r'^boundary/(?P<boundary_id>\d+)/(?P<permissionType>\w+)/(?P<assessment_id>\d+)/?$',
                           KLP_Institution_Boundary),
                       url(r'^institution-category/creator/?$',
                           KLP_Institution_Category_Create),
                       url(r'^institution-management/creator/?$',
                           KLP_Institution_Management_Create),
                       url(r'^audit/trial/$', KLP_audit),
                       url(r'^delete/(?P<model_name1>\w+)/(?P<referKey>\d+)/$',
                           KLP_Delete(permitted_methods=('POST', 'GET'))),
                       url(r'^createnew/(?P<model_name>\w+)/(?P<new_id>\d+)/$',
                           KLP_Create_Node(permitted_methods=('POST', 'GET'))),
                       url(r'^google/Secure/$', KLP_glogin),
                       url(r'^facebook/login.php/$', KLP_flogin),
                       url(r'^map/sg/as/$', KLP_Map_SG),
                       url(r'^assign/permissions/?$', KLP_Assign_Permissions),
                       url(r'^list/users/?$', KLP_Users_list),
                       url(r'^user/(?P<user_id>\d+)/delete?$', KLP_User_Delete),
                       url(r'^user/(?P<user_id>\d+)/activateuser?$', KLP_User_Activate),
                       url(r'^user/(?P<user_id>\d+)/permissions/?$',
                           KLP_User_Permissions),
                       url(r'^list/(?P<boundary_id>\d+)/user/(?P<user_id>\d+)/permissions/?$',
                           KLP_Show_Permissions),
                       url(r'^revoke/user/(?P<permissionType>\w+)/?$',
                           KLP_Revoke_Permissions),
                       url(r'^assign/user/(?P<permissionType>\w+)/?$',
                           KLP_ReAssign_Permissions),
                       url(r'^show/(?P<boundary_id>\d+)/user/(?P<user_id>\d+)/permissions/?$',
                           KLP_Show_User_Permissions),
                       url(r'^language/creator/?$', KLP_Language_Create),
                       url(r'^programme/(?P<programme_id>\d+)/view/?$',
                           KLP_Programme_View),
                       url(r'^programme/creator/?$',
                           KLP_Programme_Create),
                       url(r'^programme/(?P<programme_id>\d+)/update/$',
                           KLP_Programme_Update),
                       url(r'^filter/(?P<type_id>\d+)/programms/$',
                           KLP_Get_Programms(permitted_methods=('POST', 'GET'))))
