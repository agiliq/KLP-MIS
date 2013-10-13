#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
StaffApi is used
1) To view Individual Staff details.
2) To create new Staff
3) To update existing Staff
4) To list Staffs under institution
"""
from django.http import HttpResponse

from schools.models import *
from schools.forms import *
from vendor.django_restapi.model_resource import Collection
from vendor.django_restapi.responder import *
from vendor.django_restapi.receiver import *
from klprestApi.views.BoundaryApi import ChoiceEntry
from schools.receivers import KLP_user_Perm


class KLP_Staff(Collection):

    """To get Paricular Staff """

    def get_entry(self, staff_id):

        # Query For Selected Staff based on staff_id

        staff = Staff.objects.get(id=int(staff_id))
        return ChoiceEntry(self, staff)


def KLP_Staff_View(request, staff_id):
    """ To View Selected staff staff/(?P<staff_id>\d+)/view/$"""

    kwrg = {'is_entry': True}

        # before Staff.objects.all()

    resp = KLP_Boundary(queryset=Staff.objects.filter(pk=staff_id),
                        permitted_methods=('GET', 'POST'),
                        responder=TemplateResponder(
                            template_dir='viewtemplates',
                            template_object_name='staff'))(request,
                                                           staff_id, **kwrg)
    return HttpResponse(resp)


def KLP_Staff_Create(request, referKey):
    """ To Create New Staff institution/(?P<referKey>\d+)/staff/creator/"""

    # Checking user Permissions for Staff creation

    KLP_user_Perm(request.user, 'Staff', 'Add')
    buttonType = request.POST.get('form-buttonType')
    url = '/institution/%s/staff/creator/' % referKey
    extra_dict = {'buttonType': buttonType, 'referKey': referKey,
                  'url': url}
    extra_dict['institution_id'] = referKey
    extra_dict['stgrps'] = \
        StudentGroup.objects.filter(institution__id=referKey,
                                    active=2).order_by('name', 'section')
    institutionObj = Institution.objects.get(pk=referKey)
    if institutionObj.boundary.boundary_category.boundary_category.lower() == 'circle':

        # if the boundary category is circle get anganwadi staff types.

        extra_dict['institutionType'] = 'Anganwadi'
        Staff_Types = Staff_Type.objects.filter(category_type=2)
    else:

        # if the boundary category is not circle get Institution staff types.

        extra_dict['institutionType'] = 'Institution'
        Staff_Types = Staff_Type.objects.filter(category_type=1)
    extra_dict['Staff_Types'] = Staff_Types

        # before Staff.objects.all()

    KLP_Create_Staff = KLP_Staff(queryset=Staff.objects.filter(pk=0),
                                 permitted_methods=('GET', 'POST'),
                                 responder=TemplateResponder(
                                     template_dir='viewtemplates',
                                     template_object_name='staff',
                                     extra_context=extra_dict),
                                 receiver=XMLReceiver())

    response = \
        KLP_Create_Staff.responder.create_form(request,
                                               form_class=Staff_Form)
    return HttpResponse(response)


def KLP_staff_list(request, institution_id):
    """ To view list of staff in school
                school/(?P<school_id>\d+)/staff/view/"""

    queryset = Staff.objects.filter(institution__id=institution_id,
                                    active=2).order_by('first_name')
    url = '/institution/%s/staff/view/' % institution_id
    val = Collection(queryset, permitted_methods=('GET', 'POST'),
                     responder=TemplateResponder(
                         paginate_by=10,
                         template_dir='viewtemplates',
                         template_object_name='staff',
                         extra_context={'url': url}),
                     entry_class=ChoiceEntry)
    return HttpResponse(val(request))


def KLP_Staff_Update(request, staff_id):
    """ To update Selected staff staff/(?P<staff_id>\d+)/update/"""

    # Checking user Permissions for Staff update

    KLP_user_Perm(request.user, 'Staff', 'Update')
    buttonType = request.POST.get('form-buttonType')
    referKey = request.POST.get('form-0-boundary')
    querysetstaff = Staff.objects.filter(pk=staff_id)
    staff = querysetstaff[0]  # Staff.objects.get(pk=staff_id)
    stgrps = StudentGroup.objects.filter(
        institution=staff.institution, active=2)
    institutionObj = staff.institution
    if institutionObj.boundary.boundary_category.boundary_category.lower() == 'circle':

        # if the boundary category is circle get anganwadi staff types.

        institutionType = 'Anganwadi'
        Staff_Types = Staff_Type.objects.filter(category_type=2)
    else:

        # if the boundary category is not circle get Institution staff types.

        institutionType = 'Institution'
        Staff_Types = Staff_Type.objects.filter(category_type=1)

        # before Staff.objects.all()

    KLP_Edit_Staff = KLP_Staff(queryset=querysetstaff,
                               permitted_methods=('GET', 'POST'),
                               responder=
                               TemplateResponder(
                                   template_dir=
                                   'edittemplates',
                                   template_object_name='staff',
                                   extra_context={'buttonType': buttonType,
                                                  'referKey': referKey,
                                                  'stgrps': stgrps,
                                                  'institutionType':
                                                  institutionType,
                                                  'Staff_Types':
                                                  Staff_Types, }),
                               receiver=XMLReceiver())
    response = \
        KLP_Edit_Staff.responder.update_form(request,
                                             pk=staff_id,
                                             form_class=Staff_Form)
    return HttpResponse(response)
