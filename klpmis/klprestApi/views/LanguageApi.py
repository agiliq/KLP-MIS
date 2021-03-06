#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
LanguageApi is used to create new language
"""
from django.http import HttpResponse

from vendor.django_restapi.model_resource import Collection
from vendor.django_restapi.receiver import XMLReceiver
from vendor.django_restapi.responder import TemplateResponder
from schools.models import Moi_Type
from schools.forms import Moi_Type_Form
from klprestApi.views.BoundaryApi import ChoiceEntry


class KLP_Language(Collection):

    """ To create new language language/creator/"""

    def get_entry(self, language_id):
        language = Moi_Type.objects.all(id=language_id)
        return ChoiceEntry(self, language)


def KLP_Language_Create(request):
    """ To Create new language language/creator/"""

    buttonType = request.POST.get('form-buttonType')

        # Moi_Type.objects.all()

    KLP_Language_Create = \
        KLP_Language(queryset=Moi_Type.objects.filter(pk=0),
                     permitted_methods=('GET', 'POST'),
                     responder=TemplateResponder(
                         template_dir='viewtemplates',
                         template_object_name='Language',
                         extra_context={'buttonType': buttonType}),
                     receiver=XMLReceiver())
    response = KLP_Language_Create.responder.create_form(request,
                                                         form_class=
                                                         Moi_Type_Form)
    return HttpResponse(response)
