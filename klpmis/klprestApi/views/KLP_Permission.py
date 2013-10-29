#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
KLP_Permission file is used
1) To assign permissions
2) To list users
3) To Delete users
4) To show permissions at diffrent level of boundaries
5) To revoke user permissions
6) To reassign permissions to user.
"""
import simplejson
from subprocess import Popen

from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User
from django.forms.models import modelformset_factory

from schools.models import Assessment, Assessment_Class_Association,\
    Assessment_Institution_Association, Assessment_StudentGroup_Association,\
    Institution, StudentGroup, UserAssessmentPermissions
from schools.forms import UserAssessmentPermissions_Form, Boundary_Type
from schools.receivers import KLP_user_Perm
from klprestApi.views.TreeMenu import getAssSG
from klpmis.settings import PROJECT_ROOT, PYTHON_PATH


def KLP_Assign_Permissions(request):
    """ This method is used to assign permissions"""

    KLP_user_Perm(request.user, 'Users', None)
    respDict = {}

    deUserList = request.POST.getlist('assignToUser')
    permissions = request.POST.getlist('userPermission')
    receiver = settings.REPORTMAIL_RECEIVER
    receiver = ','.join(str(v1) for v1 in receiver)
    message = 'A mail will be sent to %s as soon as all \
                the permissions are assigned' % receiver
    permissionType = request.POST.get('permissionType')
    assessmentId = request.POST.get('assessmentId')
    bound_cat = request.POST.get('bound_cat')
    inst_list = request.POST.getlist('instName')
    bound_list = request.POST.getlist('boundaryName')
    assessmentPerm = request.POST.get('assessmentPerm')

    (count, asmCount, assignedAsmIds) = (0, 0, [])

    bound_list = ','.join(str(v1) for v1 in bound_list if v1 > 0)
    permissions = ','.join(str(v1) for v1 in permissions if v1 > 0)
    deUserList = ','.join(str(v1) for v1 in deUserList if v1 > 0)

    if not deUserList:
        respDict['respMsg'] = 'Select Atleast One User'
        respDict['isSuccess'] = False
    elif not permissions:
        respDict['respMsg'] = 'Select Atleast One Permission'
        respDict['isSuccess'] = False
    elif bound_cat in ['district', 'block', 'project']:
        if not bound_list:
            respDict['respMsg'] = 'Select Atleast One Boundary'
            respDict['isSuccess'] = False
        else:
            Popen([PYTHON_PATH,
                   PROJECT_ROOT + '/manage.py',
                   'KLP_assignPermissions', str(inst_list),
                   str(deUserList), str(permissions),
                   str(permissionType), str(assessmentId),
                   str(assessmentPerm), bound_cat, bound_list,
                   request.user.username,
                   str(request.user.id), request.path_info])

            respDict['respMsg'] = message
            respDict['isSuccess'] = True
    else:
        if not inst_list:
            respDict['respMsg'] = 'Select Atleast One Institution'
            respDict['isSuccess'] = False
        else:
            count = count + len(inst_list)
            inst_list = ','.join(str(v1) for v1 in inst_list if v1 > 0)
            Popen(['python',
                   PROJECT_ROOT + '/manage.py',
                   'KLP_assignPermissions', str(inst_list),
                   str(deUserList), str(permissions),
                   str(permissionType), str(assessmentId),
                   str(assessmentPerm),
                   bound_cat, str(bound_list).strip(),
                   request.user.username, str(request.user.id),
                   request.path_info])
            respDict['respMsg'] = message
            respDict['isSuccess'] = True

    return HttpResponse(simplejson.dumps(respDict),
                        content_type='application/json; charset=utf-8')


def assignPermission(inst_list, deUserList, permissions,
                     permissionType,
                     assessmentId=None,
                     assessmentPerm=None, username=None,
                     userId=None, path_info='/'):

    assignedInsIds = []
    allassignIds = []
    newlyassignInst = []
    if assessmentId:
        assessmentObj = Assessment.objects.get(pk=assessmentId)
        allassignIds.append(assessmentId)
    dic = {}
    for inst_id in inst_list:
        inst_id = int(inst_id)
        instObj = Institution.objects.get(pk=inst_id)
        if assessmentId:
            asmIds = []
            asmIds.append(assessmentId)
        elif permissionType != 'permissions' or assessmentPerm == 'True':
            sg_list = \
                StudentGroup.objects.filter(
                    institution__id=inst_id,
                    active=2).values_list('id', flat=True).distinct()
            asmIdSG = \
                Assessment_StudentGroup_Association.objects.filter(
                    student_group__id__in=sg_list,
                    active=2,
                    assessment__active=2).values_list('assessment__id',
                                                      flat=True).distinct()
            asmIdCl = \
                Assessment_Class_Association.objects.filter(
                    student_group__id__in=sg_list,
                    active=2,
                    assessment__active=2).values_list('assessment__id',
                                                      flat=True).distinct()
            asmInt = \
                Assessment_Institution_Association.objects.filter(
                    institution__id=inst_id,
                    active=2,
                    assessment__active=2).values_list('assessment__id',
                                                      flat=True).distinct()
            asmIds = list(set(asmIdSG) | set(asmIdCl) | set(asmInt))
        else:
            asmIds = []
        assignedInsIds.append(inst_id)
        for deUser in deUserList:
            deUser = int(deUser)
            userObj = User.objects.get(id=deUser)
            alreadyssignInst = []
            newlyassignInst = []
            AssalreadyssignInst = []
            AssnewlyassignInst = []
            Assdic = {}
            if 1:

                if permissionType == 'permissions':
                    (assCheck, sgInstList) = \
                        assessmentPermisionCheck(userObj, instObj, [],
                                                 permissions,
                                                 'permissionType')
                    if assCheck:
                        alreadyssignInst.append(inst_id)
                    else:
                        newlyassignInst.append(inst_id)

                if 1:  # assessmentPerm not in ['None',None,'']:
                    for asmId in asmIds:
                        (permissionType == 'assessmentpermissions',
                         instObj.id, 'uuuuuuuuuuuu')
                        assessmentObj = Assessment.objects.get(id=asmId)
                        if permissionType != 'permissions':
                            (assCheck, sgInstList) = \
                                assessmentPermisionCheck(userObj,
                                                         instObj,
                                                         asmId,
                                                         permissions,
                                                         permissionType)
                            if assCheck:
                                alreadyssignInst.append(inst_id)
                            else:
                                newlyassignInst.append(inst_id)
                        if sgInstList and assessmentId or assessmentId \
                                in [None, 'None', '']:
                            UserPermForm = modelformset_factory(
                                UserAssessmentPermissions,
                                form=UserAssessmentPermissions_Form)

                            requestcopy = {}  # request.POST.copy()
                            requestcopy['form-0-user'] = userObj.id
                            requestcopy['form-0-instituion'] = instObj.id
                            requestcopy[
                                'form-0-assessment'] = assessmentObj.id
                            requestcopy['form-TOTAL_FORMS'] = 1
                            requestcopy['form-MAX_NUM_FORMS'] = 1000
                            requestcopy['form-0-access'] = True
                            requestcopy['form-0-current_user'] = userId
                            requestcopy['form-0-username'] = ''
                            requestcopy['form-0-path_info'] = '/'

                            permObj = \
                                UserAssessmentPermissions.objects.filter(
                                    user=userObj,
                                    instituion=instObj,
                                    assessment=assessmentObj)
                            if permObj:
                                requestcopy['form-INITIAL_FORMS'] = 1
                                requestcopy['form-0-id'] = permObj[0].id
                                rform = UserPermForm(requestcopy,
                                                     requestcopy,
                                                     queryset=permObj)
                                AssalreadyssignInst.append(inst_id)
                            else:
                                requestcopy['form-INITIAL_FORMS'] = 0
                                rform = UserPermForm(requestcopy,
                                                     requestcopy)
                                AssnewlyassignInst.append(inst_id)

                            rform.save()
                        Assdic[asmId] = \
                            [list(set(AssalreadyssignInst)),
                             list(set(AssnewlyassignInst))]
                    if asmIds:
                        allassignIds = list(set(allassignIds)
                                            | set(asmIds))

            if (userObj, deUser) in dic:
                asdic = dic[(userObj, deUser)][0]
                for k in asdic:
                    if k in Assdic:
                        Assdic[k][0] = list(set(Assdic[k][0])
                                            | set(asdic[k][0]))
                        Assdic[k][1] = list(set(Assdic[k][1])
                                            | set(asdic[k][1]))
                    else:
                        Assdic[k] = asdic[k]

                alreadyssignInst = list(set(alreadyssignInst)
                                        | set(dic[(userObj, deUser)][1]))
                newlyassignInst = list(set(newlyassignInst)
                                       | set(dic[(userObj, deUser)][2]))
            dic[(userObj, deUser)] = [Assdic, alreadyssignInst,
                                      newlyassignInst]
    return (assignedInsIds, allassignIds, dic)


def assessmentPermisionCheck(userObj, instObj, asmId,
                             permissions,
                             permissionType):
    sgInstList = []
    if permissionType == 'assessmentpermissions':
        sgInstList = getAssSG([asmId], instObj.id)

    flag = 0
    if sgInstList and permissionType == 'assessmentpermissions' \
        or permissionType == 'permissionType' or asmId \
            and permissionType == 'assessmentpermissions':
        if not userObj.has_any_perms(instObj, perms=permissions):
            userObj.set_perms(permissions, instObj)
            flag = 1
        else:
            flag = 0
    return (flag, sgInstList)


def KLP_Users_list(request):
    """ This method is used to list out active(1) users
    other than staff and super users"""

    user = request.user
    if user.id:
        KLP_user_Perm(request.user, 'Users', None)
        user_list = User.objects.filter(is_staff=0,
                                        is_superuser=0).order_by('username')
        return render(request,
                      'viewtemplates/show_users_form.html',
                      {'user_list': user_list,
                       'user': user,
                       'title': 'KLP Users',
                       'legend': 'Karnataka Learning Partnership',
                       'entry': 'Add'})
    else:
        return HttpResponseRedirect('/login/')


def KLP_User_Activate(request, user_id):
    """ This method is used to (activate) user"""
    user = request.user
    if user.id:
        KLP_user_Perm(request.user, 'Users', None)
        userObj = User.objects.get(pk=user_id)
        userObj.is_active = 1
        userObj.save()
        return render(request,
                      'viewtemplates/userAction_done.html',
                      {'user': request.user,
                       'selUser': userObj,
                       'message': 'User Activated Successfully',
                       'legend': 'Karnataka Learning Partnership',
                       'entry': 'Add'})
    else:
        return HttpResponseRedirect('/login/')


def KLP_User_Delete(request, user_id):
    """ This method is used to delete(deactivate) user"""
    user = request.user
    if user.id:
        KLP_user_Perm(request.user, 'Users', None)
        import random
        import string
        rangeNum = 8
        randomStr = ''.join(random.choice(string.ascii_uppercase
                            + string.digits) for x in range(rangeNum))
        userObj = User.objects.get(pk=user_id)
        userObj.is_active = 0
        userObj.save()
        return render(request,
                      'viewtemplates/userAction_done.html',
                      {'user': request.user,
                       'selUser': userObj,
                       'message': 'User Deletion Successful',
                       'legend': 'Karnataka Learning Partnership',
                       'entry': 'Add'})
    else:
        return HttpResponseRedirect('/login/')


def KLP_User_Permissions(request, user_id):
    """ This method is used to show tree for the
    selected user to show permissions"""
    user = request.user
    if user.id:
        KLP_user_Perm(request.user, 'Users', None)
        userObj = User.objects.get(pk=user_id)
        boundType_List = Boundary_Type.objects.all()
        try:
            sessionVal = int(request.session['session_sch_typ'])
        except:
            sessionVal = 0
        return render(request,
                      'viewtemplates/user_permissions.html',
                      {'userId': user_id,
                       'userName': userObj.username,
                       'boundType_List': boundType_List,
                       'home': True,
                       'session_sch_typ': sessionVal,
                       'entry': 'Add',
                       'shPerm': True,
                       'title': 'KLP Permissions',
                       'legend': 'Karnataka Learning Partnership'})
    else:
        return HttpResponseRedirect('/login/')


def KLP_Show_Permissions(request, boundary_id, user_id):
    """ This method is used to show user permissions """

    userObj = User.objects.get(pk=user_id)
    boundType_List = Boundary_Type.objects.all()
    try:
        sessionVal = int(request.session['session_sch_typ'])
    except:
        sessionVal = 0
    redUrl = '/list/%s/user/%s/permissions/' % (boundary_id, user_id)
    assignedInst = Institution.objects.select_related('boundary'
                                                      ).filter(Q(boundary__id=boundary_id)
                                                               | Q(boundary__parent__id=boundary_id)
                                                               | Q(boundary__parent__parent__id=boundary_id),
                     active=2).extra(where=['''schools_institution.id in (SELECT "obj_id" FROM "public"."object_permissions_institution_perms" WHERE "user_id" = '%s' AND "Acess" = '1')'''
                                            % user_id]).only('id',
                                                             'name',
                                                             'boundary').order_by('boundary',
                                                                                  'boundary__parent',
                                                                                  'name')

    assignedInstIds = assignedInst.values_list('id', flat=True)
    unAssignedInst = Institution.objects.select_related('boundary'
                                                        ).filter(Q(boundary__id=boundary_id)
                                                                 | Q(boundary__parent__id=boundary_id)
                                                                 | Q(boundary__parent__parent__id=boundary_id),
                                                                 active=2).exclude(pk__in=assignedInstIds).only('id', 'name', 'boundary').order_by('boundary',
                                                                                                                                                   'boundary__parent', 'name')

    assignedpermObjects = \
        UserAssessmentPermissions.objects.select_related('assessment',
                                                         'instituion'
                                                         ).filter(Q(instituion__boundary__id=boundary_id)
                                                                  | Q(instituion__boundary__parent__id=boundary_id)
                                                                  | Q(instituion__boundary__parent__parent__id=boundary_id),
                                                                  user=userObj, access=True).defer('access'
                                                                                                   ).order_by('instituion__boundary',
                                                                                                              'instituion__boundary__parent',
                                                                                                              'instituion__name')

    unMapObjs = \
        Assessment_StudentGroup_Association.objects.select_related('student_group', 'assessment'
                                                                   ).filter(Q(student_group__institution__boundary__id=boundary_id)
                                                                            | Q(student_group__institution__boundary__parent__id=boundary_id)
                                                                            | Q(student_group__institution__boundary__parent__parent__id=boundary_id),
                                                                            active=2).defer('active'
                                                                                            ).order_by('student_group__institution__boundary',
                                                                                                       'student_group__institution__boundary__parent',
                                                                                                       'student_group__institution__name')
    for assignedPermObj in assignedpermObjects:
        qsets = Q(assessment=assignedPermObj.assessment) \
            & Q(student_group__institution=assignedPermObj.instituion)
        unMapObjs = unMapObjs.exclude(qsets)
    unMapList = unMapObjs.values_list('student_group__institution',
                                      'assessment').distinct()

    # get all unassigned assessment objects

    qList = \
        [Assessment_StudentGroup_Association.objects.select_related('student_group', 'assessment'
                                                                    ).filter(student_group__institution__id=unMapVal[0],
         assessment__id=unMapVal[1]).defer('active')[0] for unMapVal in
         unMapList]

    return render(request,
                  'viewtemplates/show_permissions.html',
                  {'assignedInst': assignedInst,
                   'userId': user_id,
                   'userName': userObj.username,
                   'unAssignedInst': unAssignedInst,
                   'assignedpermObjects': assignedpermObjects,
                   'redUrl': redUrl,
                   'qList': qList})


def KLP_Show_User_Permissions(request, boundary_id, user_id):
    return render(request,
                  'viewtemplates/show_permissions.html',
                  {'userId': user_id,
                   'boundary_id': boundary_id,
                   'confirmMsg': True})


def KLP_Revoke_Permissions(request, permissionType):
    """ This method is used to revoke user permissions"""
    KLP_user_Perm(request.user, 'Users', None)
    user_id = request.POST.get('userId')
    opStatus = 'success'
    try:
        if permissionType == 'permissions':
            userObj = User.objects.get(pk=user_id)
            instList = request.POST.getlist('assignedInst')
            for inst_id in instList:
                instObj = Institution.objects.get(pk=inst_id)
                userObj.revoke('Acess', instObj)
        else:
            assignedAsmList = request.POST.getlist('assignedAsm')
            for userAsm_id in assignedAsmList:

                permObj = UserAssessmentPermissions.objects.get(
                    pk=userAsm_id)
                permObj.access = False  # revoke permissions
                permObj.save()
    except:
        opStatus = 'fail'
    return HttpResponse(opStatus)


def KLP_ReAssign_Permissions(request, permissionType):
    """ This method is used to reassign permissions to user"""
    KLP_user_Perm(request.user, 'Users', None)
    userList = request.POST.getlist('userId')
    permissions = ['Acess']
    opStatus = 'success'
    try:
        if permissionType == 'permissions':
            inst_list = request.POST.getlist('unassignedInst')
            (a, b, c) = assignPermission(inst_list,
                                         userList,
                                         permissions,
                                         permissionType,
                                         None,
                                         True,
                                         request.user.username,
                                         request.path_info)
        else:
            asmList = request.POST.getlist('unassignedAsm')
            for asm in asmList:
                asm_list = asm.split('_')
                inst_list = [asm_list[0]]
                assessmentId = asm_list[1]
                (a, b, c) = assignPermission(inst_list,
                                             userList,
                                             permissions,
                                             permissionType,
                                             assessmentId,
                                             None,
                                             request.user.username,
                                             request.path_info)
    except:
        opStatus = 'fail'
    return HttpResponse(opStatus)
