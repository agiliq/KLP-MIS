"""
Assessment Api file is used
1) To view Assessment Details
2) To Create new assessment
3) To Update existing assessment
4) To get list of assessment while filtering based on programme in
   filter by programme link
"""

import datetime

from django.conf.urls import patterns, url
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


from django_restapi.resource import Resource
from django_restapi.model_resource import Collection
from django_restapi.responder import TemplateResponder
from django_restapi.receiver import XMLReceiver

from schools.forms import Assessment_Form, Assessment_Lookup_Form, Question_Form
from schools.models import Assessment, Assessment_Lookup
from schools.receivers import KLP_user_Perm

from klprestApi.BoundaryApi import ChoiceEntry


class KLP_Assessment(Collection):
    def get_entry(self, assessment_id):
        assessment = Assessment.objects.get(id=assessment_id)
        return ChoiceEntry(self, assessment)


class KLP_Assessment_Lookup(Collection):
    def get_entry(self, assessment_lookup_id):
        assessment_lookup = Assessment_Lookup.objects.get(id=
                                                          assessment_lookup_id)
        return ChoiceEntry(self, assessment_lookup)


def AssessmentView(request, assessment_id):
    """ To View Selected Assessment assessment/(?P<assessment_id>\d+)/view/"""
    kwrg = {'is_entry': True}
    assessment_obj = Assessment.objects.filter(pk=assessment_id)
    assessment_lookup = Assessment_Lookup.objects.filter(assessment__id=
                                                         assessment_id)
    copyEnable = True if (not assessment_lookup
                          and assessment_obj[0].primary_field_type == 4
                          and assessment_obj[0].flexi_assessment) else False
                         # before Assessment.objects.all()

    t_responder = TemplateResponder(template_dir='viewtemplates',
                                    template_object_name='assessment',
                                    extra_context={'copyEnable':
                                                   copyEnable})
    resp = KLP_Assessment(queryset=assessment_obj,
                          permitted_methods=('GET', 'POST'),
                          responder=t_responder,)(request,
                                                  assessment_id,
                                                  **kwrg)
    return HttpResponse(resp)


def AssessmentCreate(request, referKey):
    """ To Create New Assessment
        programme/assessment/(?P<referKey>\d+)/creator/"""
    KLP_user_Perm(request.user, "Assessment", "Add")
    now = datetime.date.today()
    buttonType = request.POST.get('form-buttonType')
    currentMont = int(now.strftime('%m'))
    endYear = int(now.strftime('%Y'))
    if currentMont > 4:
        endYear = endYear + 1
        extra_context_dict = {'buttonType': buttonType,
                              'referKey': referKey,
                              'end_date': 30,
                              'endYear': endYear,
                              'endMonth': 'APRIL'}
        t_responder = TemplateResponder(template_dir='viewtemplates',
                                        template_object_name='assessment',
                                        extra_context=extra_context_dict)

        assessment = KLP_Assessment(queryset=Assessment.objects.filter(pk=0),
                                    permitted_methods=('GET', 'POST'),
                                    responder=t_responder,
                                    receiver = XMLReceiver())
        response = assessment.responder.create_form(request,
                                                    form_class=Assessment_Form)

        return HttpResponse(response)


def AssessmentLookupCreate(request, referKey):
    """ To Create New Assessment
    programme/assessment/(?P<referKey>\d+)/assessment_lookup_creator/"""
    # Checking user Permissions for Assessment add
    KLP_user_Perm(request.user, "Assessment", "Add")
    buttonType = request.POST.get('form-buttonType', '')
    assessment_lookups = Assessment_Lookup.objects.filter(
                          assessment__id=referKey).order_by('rank', 'name')
    if 1:
        rankrange = 21
        if len(assessment_lookups)+1 >= rankrange:
            rankrange = len(assessment_lookups)+2
        extra_context_dict = {'buttonType': buttonType,
                              'referKey': referKey,
                              'rankrange': range(1, rankrange),
                              'rank': len(assessment_lookups)+1}
        t_responder = TemplateResponder(template_dir='viewtemplates',
                                        template_object_name='assessment_lookup',
                                        extra_context=extra_context_dict)

        assessment = KLP_Assessment(queryset=Assessment_Lookup.objects.filter(pk=0),
                                    permitted_methods=('GET', 'POST'),
                                    responder=t_responder,
                                    receiver=XMLReceiver(),)
        response = assessment.responder.create_form(request,
                                                    form_class=Assessment_Lookup_Form)

        return HttpResponse(response)


def AssessmentLookupList(request, referKey):
    """ To View Selected StudentGroup
        studentsroup/(?P<areferKey>\d+)/view/?$"""
    reqlist = request.GET.items()
    itemlist = [str(k[0]) for k in reqlist]
    if 'count' in itemlist:
        count = request.GET['count']
    else:
        count = '0'
    #kwrg = {'is_entry': True}

    url = '/assessment_lookup/'+referKey+'/multieditor/'
    assessment_lookups = Assessment_Lookup.objects.filter(assessment__id=referKey).order_by('rank', 'name')

    Norecords = assessment_lookups.count()
    t_responder = TemplateResponder(template_dir='viewtemplates',
                                    template_object_name='assessement_lookup',
                                    paginate_by=20,
                                    extra_context={'assessment_id': referKey,
                                                   'referKey': referKey,
                                                   'url': url,
                                                   'Norecords': Norecords,
                                                   'count': count})
    resp = Collection(assessment_lookups,
                      permitted_methods=('GET', 'POST'),
                      responder=t_responder,)

    return HttpResponse(resp(request))


def AssessmentLookupMultieditor(request, assessment_id):
    """ To View Selected StudentGroup
        studentsroup/(?P<assessment_id>\d+)/edit/?$"""
    """ To show Bulk Students to update """
    assessment_lookupList = request.GET.getlist("assessment_lookup")

    context = {'assessment_id': assessment_id,
               'assessment_lookuplist': assessment_lookupList}

    return render(request,
                  'edittemplates/assessment_lookup_call_form.html',
                  context)


def KLP_Assessment_Lookup_Update(request, referKey,
                                 assessment_lookup_id, counter=0):
    """ To update Selected Boundary
    assessment/(?P<assessment_id>\d+)/update/"""
    KLP_user_Perm(request.user, "Assessment", "Update")

    buttonType = request.POST.get('form-buttonType')

    extra_context = {'buttonType': buttonType,
                     'referKey': referKey,
                     'assessment_lookup_id': assessment_lookup_id,
                     'counter': counter}
    t_responder = TemplateResponder(template_dir='edittemplates',
                                    template_object_name='assessment_lookup',
                                    extra_context=extra_context)

    assessment = KLP_Assessment(queryset=Assessment_Lookup.objects.filter(pk=assessment_lookup_id).order_by('rank', 'name'),
                                permitted_methods=('GET', 'POST'),
                                responder=t_responder,
                                receiver=XMLReceiver(),)

    response = assessment.responder.update_form(request,
                                                pk=assessment_lookup_id,
                                                form_class=Assessment_Lookup_Form)

    return HttpResponse(response)


def AssessmentUpdate(request, assessment_id):
    """ To update Selected Boundary
    assessment/(?P<assessment_id>\d+)/update/"""
    # Checking user Permissions for Assessment Update
    KLP_user_Perm(request.user, "Assessment", "Update")
    # Get Current date for to pass for calendar
    now = datetime.date.today()
    buttonType = request.POST.get('form-buttonType')
    referKey = request.POST.get('form-0-programme')
    currentMont = int(now.strftime('%m'))
    endYear = int(now.strftime('%Y'))
    if currentMont > 4:
        endYear = endYear + 1

    extra_context_dict = {'buttonType': buttonType,
                          'referKey': referKey,
                          'end_date': 30,
                          'endYear': endYear,
                          'endMonth': 'APRIL'}
    t_responder = TemplateResponder(template_dir='edittemplates',
                                    template_object_name='assessment',
                                    extra_context=extra_context_dict)

    assessment = KLP_Assessment(queryset=Assessment.objects.filter(pk=assessment_id),
                                permitted_methods=('GET', 'POST'),
                                responder=t_responder,
                                receiver = XMLReceiver(),)
    response = assessment.responder.update_form(request, pk=assessment_id,
                                                form_class=Assessment_Form)

    return HttpResponse(response)


class KLP_Get_Assessments(Resource):
    """ To get  assessment under programme
        filter/programme/(?P<programme_id>\d+)/assessments/"""
    def read(self, request, programme_id):
        try:
            # Query all active(2) assessments based on programme id
            assessments_list = Assessment.objects.filter(programme__id=programme_id,
                                                         active=2).defer("programme")
            respStr = ''
            for assessment in assessments_list:
                respStr += '%s$$%s&&' % (assessment.id, assessment)
            # slice string to remove "&&" added at last of string
            return HttpResponse(respStr[0:len(respStr)-2])
        except:
            return HttpResponse('fail')


@csrf_exempt
def KLP_lookup_inlineEdit(request):
    lookupId = request.POST.get('lookupId', 0)
    name = request.POST.get('name', 0)
    des = request.POST.get('des', 0)
    lookObj = Assessment_Lookup.objects.get(id=int(lookupId))
    lookObj.name = name
    lookObj.description = des
    lookObj.rank = request.POST.get('rank', 0)
    try:
        lookObj.save()
    except IntegrityError:
        return HttpResponse('Value is already existing')
    return HttpResponse('Data Saved')


@csrf_exempt
def AssessmentLookupCopy(request, referKey):
    """ To View Selected StudentGroup
    studentsroup/(?P<areferKey>\d+)/copy/?$'/assessment/assessment_lookup/'+stre(referKey+'/view',"""

    if request.POST:
        assessment_id = request.POST.get('lookupValues')
        assessment_lookups = Assessment_Lookup.objects.filter(assessment__id=assessment_id)

        for k in assessment_lookups:
            k.id = None
            k.assessment_id = referKey
            k.save()

        return HttpResponse('Copied Successfully')
    else:
        assessment_lookups = Assessment_Lookup.objects.filter().values_list('assessment', flat=True)
        assessment_list = Assessment.objects.filter(id__in=assessment_lookups).exclude(id=referKey)
        context = {'assessment_id': referKey,
                   'assessmentList': assessment_list}
        return render(request,
                      'viewtemplates/assessment_lookup_copy.html',
                      context)


@csrf_exempt
def KLP_copy_Assessments(request, assessment_id):
    """To copy the assessment"""
    assessment = Assessment.objects.filter(id=assessment_id)[0]

    if request.POST:
        try:
            KLP_user_Perm(request.user, "Assessment", "Create")
            assessment = Assessment.objects.filter(id=assessment_id).values()
            assessment_dic = assessment[0]
            del assessment_dic['id']
            assessment_dic['programme'] = assessment_dic['programme_id']
            assessment_dic['name'] = request.POST.get('newasssmentname',
                                                      'copy _of_')
            assessment_form = Assessment_Form(assessment_dic)
            new_assessment = assessment_form.save()
            questions = Question.objects.filter(assessment__id=assessment_id).values()
            newquestionids = ''
            for question in questions:
                del question['id']
                question['assessment'] = new_assessment.id
                qq = Question_Form(question)
                question_obj = qq.save()
                newquestionids += str(question_obj.id)+','

            AssessmentLookupCopy(request, new_assessment.id)
            msg = 'Succesfully Copied_' + str(new_assessment.id)
            msg += '_' + newquestionids
            return HttpResponse(msg)
        except:
            return HttpResponse('Duplicate Assessment .')
    else:
        context = {'assessment': assessment}
        return render(request,
                      'viewtemplates/assessment_copy_form.html',
                      context)


urlpatterns = patterns('',
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
)
