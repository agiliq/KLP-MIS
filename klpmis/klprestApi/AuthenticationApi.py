"""
AuthenticationApi is used
1) To login
2) To logout
3) To check user is logged in or not.
"""

from django.conf.urls import patterns, url
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render


def klp_login(request):
    """ This method is for user login """

    context = {}
    context['title'] = 'Karnataka Learning Partnership'
    context['legend'] = 'Karnataka Learning Partnership'
    context['entry'] = 'Add'
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
                context['message'] = 'Your account is not active, contact the administrator'
        else:
            context['message'] = 'Please enter a correct username and password'
    return render_to_response('login.html', context, context_instance=RequestContext(request))


def klp_logout(request):
    """ This method is for user logout """

    logout(request)
    context = {'title': 'Karnataka Learning Partnership',
               'legend': 'Karnataka Learning Partnership',
               'entry': 'Add'}
    return render(request,
                  'login.html',
                  context)


def klp_user_auth(request):
    """ This method checks, user is authenticated or not """
    return HttpResponse(request.user.is_authenticated())


urlpatterns = patterns('',
                       url(r'^login/?$', klp_login, name="login"),
                       url(r'^logout/?$', klp_logout, name="logout"),
                       url(r'^user/authentication/?$', klp_user_auth)
                       )
