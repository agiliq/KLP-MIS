#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.http import HttpResponse

from schools.models import Assessment, StudentGroup,\
    Assessment_StudentGroup_Association


def KLP_Map_SG(request):
    """ This method uses to map Student Groups With Assessment"""

    boundary_id = request.GET.get('boundary')
    asssessment_id = request.GET.get('assessment')
    assessmentObj = Assessment.objects.get(id=asssessment_id)
    studentgroup_list = \
        StudentGroup.objects.filter(
            institution__boundary__parent__parent__id=boundary_id)
    for sg in studentgroup_list:
        sg_as_mapObj = \
            Assessment_StudentGroup_Association(assessment=assessmentObj,
                                                student_group=sg, active=2)
        sg_as_mapObj.save()
    return HttpResponse(studentgroup_list)
