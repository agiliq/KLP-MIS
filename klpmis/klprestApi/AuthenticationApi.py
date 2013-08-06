#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
AuthenticationApi is used
1) To login
2) To logout
3) To check user is logged in or not.
"""

from django.conf.urls.defaults import *
from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect

from django_restapi.responder import *
from django_restapi.receiver import *

from schools.models import *
from schools.forms import *


class Redirect_View(TemplateView):
    template_name = "login.html"


def klp_login(request):
    """ This method is for user login """

    user = request.user
    if request.method == 'POST':
        user = authenticate(username=request.POST['username'],
                            password=request.POST['password'])
        if user is not None:
            if user.is_active:
                login(request, user)
                usrUrl = {'Data Entry Executive': '/home/',
                          'Data Entry Operator': '/home/?respType=filter',
                          'AdminGroup': '/home/?respType=userpermissions'}
                if user.is_superuser or user.is_staff:
                # If user is super user or staff redirect
                # to home page after login.
                    return HttpResponseRedirect('/home/')
                else:
                # else redirect to respective paths defined
                # in usrUrl dictionary based on group.
                    userGroup = user.groups.all().defer('user',
                                                        'permissions')[0].name
                    return HttpResponseRedirect(usrUrl[userGroup])
            else:
                context = {'message': 'Please enter a \
                                     correct username and password',
                           'title': 'Karnataka Learning Partnership',
                           'legend': 'Karnataka Learning Partnership',
                           'entry': 'Add'}
                return render(request,
                              'login.html',
                              context)
        else:
            context = {'message': 'Please enter a \
                                correct username and password',
                       'title': 'Karnataka Learning Partnership',
                       'legend': 'Karnataka Learning Partnership',
                       'entry': 'Add'}
            return render(request,
                          'login.html',
                          context)
    else:
        context = {'user': user,
                   'title': 'Karnataka Learning Partnership',
                   'legend': 'Karnataka Learning Partnership',
                   'entry': 'Add'}
        return render(request,
                      'login.html',
                      context)


def KLP_Logout_user(request):
    """ This method is for user logout """

    logout(request)
    context = {'title': 'Karnataka Learning Partnership',
               'legend': 'Karnataka Learning Partnership',
               'entry': 'Add'}
    return render(request,
                  'login.html',
                  context)


def KLP_User_Auth(request):
    """ This method checks, user is authenticated or not """
    return HttpResponse(request.user.is_authenticated())


urlpatterns = patterns('',
                       url(r'^login/?$', klp_login, name="login"),
                       url(r'^logout/?$', KLP_Logout_user),
                       url(r'^user/authentication/?$', KLP_User_Auth))
