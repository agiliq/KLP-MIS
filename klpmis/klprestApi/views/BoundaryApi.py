#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Boundary Api is used
1) To view Individual Boundary details
2) To create new boundary
3) To update existing boundary
"""
from django.http import HttpResponse
from crispy_forms.layout import Submit

from vendor.django_restapi.model_resource import Collection, Entry
from vendor.django_restapi.responder import TemplateResponder
from vendor.django_restapi.receiver import XMLReceiver
from schools.receivers import KLP_user_Perm
from schools.forms import Boundary_Form, BoundaryFormHelper
from schools.models import Boundary, Boundary_Type


class ChoiceEntry(Entry):

    pass


class KLP_Boundary(Collection):

    """To get Selected Boundary """

    def get_entry(self, boundary_id):

        # Query For selected boundary based on boundary_id

        boundary = \
            Boundary.objects.filter(id=int(boundary_id)).defer('boundary')[0]
        return ChoiceEntry(self, boundary)


def KLP_Boundary_View(request, boundary_id, boundarytype_id):
    """ To View Selected Boundary boundary/(?P<boundary_id>\d+)/(
            ?P<boundarytype_id>\d+)/view/$"""

    kwrg = {'is_entry': True}
    boundaryTypObjquery = \
        Boundary_Type.objects.filter(pk=boundarytype_id)
    boundaryTypObj = boundaryTypObjquery[0]
    resp = \
        KLP_Boundary(queryset=Boundary.objects.filter(
            pk=boundary_id).defer('boundary'),
            permitted_methods=('GET', 'POST'),
            responder=TemplateResponder(
                template_dir='viewtemplates',
                template_object_name='boundary',
                extra_context={
                    'boundary_type':
                    boundaryTypObj.boundary_type}))(request, boundary_id,
                                                    **kwrg)
    return HttpResponse(resp)


def KLP_Boundary_Create(request):
    """ To Create New Boundary boundary/creator/"""

    # Checking user Permissions

    KLP_user_Perm(request.user, 'Boundary', 'Add')
    buttonType = request.POST.get('form-buttonType')
    KLP_Create_Boundary = \
        KLP_Boundary(queryset=Boundary.objects.filter(pk=0),
                     permitted_methods=('GET', 'POST'),
                     responder=TemplateResponder(
                         template_dir='viewtemplates', template_object_name=
                         'boundary',
                         extra_context={'buttonType': buttonType}),
                     receiver=XMLReceiver())

    helper = BoundaryFormHelper()
    helper.form_tag = False

    response = KLP_Create_Boundary.responder.create_form(
        request, form_class=Boundary_Form, form_helper=helper)

    return HttpResponse(response)


def KLP_Boundary_Update(request, boundary_id):
    """ To update Selected Boundary boundary/(?P<boundary_id>\d+)/update/"""

    # Checking user Permissions

    KLP_user_Perm(request.user, 'Boundary', 'Update')
    buttonType = request.POST.get('form-buttonType')
    referKey = request.POST.get('form-0-boundary')
    KLP_Edit_Boundary = \
        KLP_Boundary(queryset=Boundary.objects.filter(
            pk=boundary_id).defer('boundary'),
            permitted_methods=('GET', 'POST'),
            responder=TemplateResponder(template_dir='edittemplates',
                                        template_object_name='boundary',
                                        extra_context={
                                            'buttonType': buttonType,
                                            'referKey': referKey}),
            receiver=XMLReceiver())

    response = \
        KLP_Edit_Boundary.responder.update_form(request, pk=boundary_id,
                                                form_class=Boundary_Form)

    return HttpResponse(response)
