#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
InstitutionCategoryApi is used to create new Institution Category
"""
from django.http import HttpResponse

from vendor.django_restapi.model_resource import Collection
from klprestApi.views.BoundaryApi import ChoiceEntry
from vendor.django_restapi.responder import TemplateResponder
from vendor.django_restapi.receiver import XMLReceiver

from schools.models import Institution_Category
from schools.forms import Institution_Category_Form


class KLP_Institution_Category(Collection):

    """ To create new Institution Category school-category/creator/ """

    def get_entry(self, institution_category_id):
        institution_category = \
            Institution_Category.objects.all(id=institution_category_id)
        return ChoiceEntry(self, institution_category)


def KLP_Institution_Category_Create(request):
    """ To Create new institution category institution-category/creator/"""

    buttonType = request.POST.get('form-buttonType')
    category_type = request.GET.get('category_type')

        # before Institution_Category.objects.all()

    KLP_Institution_Category_Create = \
        KLP_Institution_Category(
            queryset=Institution_Category.objects.filter(pk=0),
            permitted_methods=('GET', 'POST'),
            responder=TemplateResponder(
                template_dir='viewtemplates',
                template_object_name='InstitutionCategory',
                extra_context={'buttonType': buttonType,
                               'category_type': category_type}),
            receiver=XMLReceiver())
    response = \
        KLP_Institution_Category_Create.responder.create_form(
            request, form_class=Institution_Category_Form)

    return HttpResponse(response)
