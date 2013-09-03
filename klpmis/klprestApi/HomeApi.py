"""
HomeApi is used
1) To view home page based on user roles
2) To set/change session value on change of boundary type.
"""

from django.shortcuts import render
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django_restapi.resource import Resource
from schools.models import Boundary_Type, Programme


class Home(Resource):

    """ To generate Home Page home/"""

    def read(self, request):
        user = request.user
        if user.is_authenticated():
            sessionVal = int(request.session.get('session_sch_type', 0))
            respType = request.GET.get('respType')
            boundType_List = Boundary_Type.objects.all()
            klp_UserGroups = user.groups.all()
            user_GroupsList = ['%s' % usergroup.name for usergroup in
                               klp_UserGroups]
            respDict = {
                'entry': 'Add',
                'boundType_List': boundType_List,
                'session_sch_typ': sessionVal,
                'usergroups': user_GroupsList,
            }
            if not respType and (
                    user.is_superuser or
                    'Data Entry Executive' in user_GroupsList or
                    user.is_staff):
                respDict['home'] = True
                respDict['urHere'] = 'Home'
            elif respType == 'programme' and (
                    user.is_superuser or user.is_staff):
                respDict['programme'] = True
                respDict['urHere'] = 'Programme'
            elif respType == 'filter' and (
                    user.is_superuser or user.is_staff or
                    'Data Entry Operator' in user_GroupsList or
                    'Data Entry Executive' in user_GroupsList):
                respDict['home'] = True
                respDict['filter'] = True
                respDict['urHere'] = 'Data Entry'
                respDict['prgsList'] = Programme.objects.filter(
                    active=2, programme_institution_category=sessionVal)
            elif respType == 'userpermissions' and (
                    user.is_superuser or 'AdminGroup' in user_GroupsList):
                respDict['home'] = True
                respDict['permission'] = True
                respDict['urHere'] = 'Permissions'
            elif respType == 'assessmentpermissions' and (
                    user.is_superuser or 'AdminGroup' in user_GroupsList):
                respDict['home'] = True
                respDict['filter'] = True
                respDict['assessmentpermission'] = True
                respDict['urHere'] = 'Assessment Permissions'
                respDict['prgsList'] = Programme.objects.filter(
                    active=2, programme_institution_category=sessionVal)
            elif respType == 'createUser' and (
                    user.is_superuser or 'AdminGroup' in user_GroupsList):
                return HttpResponseRedirect(reverse('accounts_add_user'))
            elif respType == 'changepermissions' and (
                    user.is_superuser or 'AdminGroup' in user_GroupsList):
                return HttpResponseRedirect('change/user/permissions')
            else:
                logout(request)
                return HttpResponseRedirect('/login/')

            return render(request,
                          'viewtemplates/home.html',
                          respDict)
        else:
            return HttpResponseRedirect('/login/')
