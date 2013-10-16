#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
BoundaryTypeApi is used to create new boundary type
"""
from vendor.django_restapi.model_resource import Collection
from vendor.django_restapi.responder import TemplateResponder
from vendor.django_restapi.receiver import XMLReceiver
from klprestApi.views.BoundaryApi import ChoiceEntry

from schools.models import Boundary_Type


class BoundaryTypeView(Collection):

    """ To Create New Boundary Type boundary-type/creator/"""

    def get_entry(self, boundary_type_id):
        boundary_type = Boundary_Type.objects.all(id=boundary_type_id)
        return ChoiceEntry(self, boundary_type)


# before Boundary_Type.objects.all()

template_boundary_type_view = \
    BoundaryTypeView(queryset=Boundary_Type.objects.filter(pk=0),
                     permitted_methods=('GET', 'POST'),
                     responder=TemplateResponder(
                         template_dir='viewtemplates',
                         template_object_name='boundary_type'),
                     receiver=XMLReceiver())
