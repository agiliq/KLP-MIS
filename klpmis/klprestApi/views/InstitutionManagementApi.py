#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
InstitutionManagementApi is used to create new Institution Management
"""
from django.http import HttpResponse

from vendor.django_restapi.model_resource import Collection
from schools.models import Institution_Management
from vendor.django_restapi.responder import TemplateResponder
from vendor.django_restapi.receiver import XMLReceiver
from schools.forms import Institution_Management_Form
from klprestApi.views.BoundaryApi import ChoiceEntry


class KLP_Institution_Management(Collection):

    """ To create new management institution-management/creator/"""

    def get_entry(self, institution_management_id):
        institution_management = \
            Institution_Management.objects.all(id=institution_management_id)
        return ChoiceEntry(self, institution_management)


def KLP_Institution_Management_Create(request):
    """ To Create new institution management
        institution-management/creator/"""

    buttonType = request.POST.get('form-buttonType')

        # before Institution_Mangement.objects.all()

    KLP_Institution_Management_Create = \
        KLP_Institution_Management(
            queryset=Institution_Management.objects.filter(pk=0),
            permitted_methods=('GET', 'POST'),
            responder=TemplateResponder(
                template_dir='viewtemplates',
                template_object_name='InstitutionManagement',
                extra_context={
                    'buttonType': buttonType}),
            receiver=XMLReceiver())
    response = \
        KLP_Institution_Management_Create.responder.create_form(
            request, form_class=Institution_Management_Form)

    return HttpResponse(response)
