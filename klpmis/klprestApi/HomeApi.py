"""
HomeApi is used
1) To view home page based on user roles
2) To set/change session value on change of boundary type.
"""

from django.conf.urls.defaults import patterns, url
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.http import HttpResponseRedirect

from django_restapi.resource import Resource
from schools.models import Boundary_Type, Programme


class KLP_Home(Resource):

    """ To generate Home Page home/"""

    def read(self, request):
        user = request.user
        if user.is_authenticated():
            try:
                sessionVal = int(request.session['session_sch_typ'])
            except:
                sessionVal = 0
            respType = request.GET.get('respType') or None

        # Get all Boundary Types

            boundType_List = Boundary_Type.objects.all()

        # Get Logged in user group

            klp_UserGroups = user.groups.all()
            user_GroupsList = ['%s' % usergroup.name for usergroup in
                               klp_UserGroups]
            respDict = {
                'legend': 'Karnataka Learning Partnership ',
                'title': 'Karnataka Learning Partnership ',
                'entry': 'Add',
                'boundType_List': boundType_List,
                'session_sch_typ': sessionVal,
                'user': user,
                'usergroups': user_GroupsList,
                }
            if respType == None and (user.is_superuser
                    or 'Data Entry Executive' in user_GroupsList
                    or user.is_staff):
                respDict['home'] = True
                respDict['urHere'] = 'Home'
            elif respType == 'programme' and (user.is_superuser
                    or user.is_staff):
                respDict['programme'] = True
                respDict['urHere'] = 'Programme'
            elif respType == 'filter' and (user.is_superuser
                    or user.is_staff or 'Data Entry Operator'
                    in user_GroupsList or 'Data Entry Executive'
                    in user_GroupsList):
                respDict['home'] = True
                respDict['filter'] = True
                respDict['urHere'] = 'Data Entry'
                respDict['prgsList'] = \
                    Programme.objects.filter(active=2,
                        programme_institution_category=sessionVal)
            elif respType == 'userpermissions' and (user.is_superuser
                    or 'AdminGroup' in user_GroupsList):
                respDict['home'] = True
                respDict['permission'] = True
                respDict['urHere'] = 'Permissions'
            elif respType == 'assessmentpermissions' \
                and (user.is_superuser or 'AdminGroup'
                     in user_GroupsList):
                respDict['home'] = True
                respDict['filter'] = True
                respDict['assessmentpermission'] = True
                respDict['urHere'] = 'Assessment Permissions'
                respDict['prgsList'] = \
                    Programme.objects.filter(active=2,
                        programme_institution_category=sessionVal)
            elif respType == 'createUser' and (user.is_superuser
                    or 'AdminGroup' in user_GroupsList):
                return HttpResponseRedirect('accounts/auth/user/add/')
            elif respType == 'changepermissions' and (user.is_superuser
                    or 'AdminGroup' in user_GroupsList):
                return HttpResponseRedirect('change/user/permissions')
            else:
                logout(request)
                return HttpResponseRedirect('/login/')

            respTemplate = render_to_response('viewtemplates/home.html'
                    , respDict)
            return HttpResponse(respTemplate)
        else:

        # If user is not login redirects to login page

            return HttpResponseRedirect('/login/')


def KLP_Set_Session(request):
    """ This method uses for set the session """

    request.session['session_sch_typ'] = request.GET.get('sessionVal')
    return HttpResponse('Success')


urlpatterns = patterns('',
    url(r'^home/$', KLP_Home(permitted_methods=('GET',))),
    url(r'^set/session/$', KLP_Set_Session)
)
