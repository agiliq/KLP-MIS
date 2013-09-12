from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, render_to_response
from django.conf.urls.defaults import *
from django.template import RequestContext

from schools.models import *
from schools.forms import UserCreationFormExtended


def login(request):
    """ This method is for user login """

    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    context = {'entry': 'Add'}
    form = AuthenticationForm()
    if request.method == 'POST':
        form = AuthenticationForm(None, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            django_login(request, user)
            return HttpResponseRedirect(reverse('home'))
    context['form'] = form
    return render(request,
                  'login.html',
                  context)


def logout(request):
    """ This method is for user logout """

    django_logout(request)
    return HttpResponseRedirect(reverse('login'))


def user_auth(request):
    """ This method checks, user is authenticated or not """
    return HttpResponse(request.user.is_authenticated())


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('login'))


def add_user(request,
             template_name='viewtemplates/add_new_user.html',
             post_change_redirect=None):

    """ This method is used to create or add new user """
    user = request.user
    klp_UserGroups = user.groups.all()
    user_GroupsList = ['%s' % usergroup.name for usergroup in
                       klp_UserGroups]
    if user.id is not None and (user.is_superuser or 'AdminGroup'
                                in user_GroupsList):

        # if user is login and user is super user or in admin group

        if post_change_redirect is None:
            post_change_redirect = \
                reverse('accounts_add_user_done')
        if request.method == 'POST':

            # Get Data From Form
            form = UserCreationFormExtended(request.POST)
            if form.is_valid():

                # if form is valid save data     ....       ....          ....

                form.save()
                return HttpResponseRedirect(post_change_redirect)
            else:

                # else redirect back to add new user form

                return render_to_response(template_name, {
                    'form': form,
                    'title': 'KLP User',
                    'legend': 'Karnataka Learning Partnership',
                    'entry': 'Add', },
                    context_instance=RequestContext(request))
        else:
            form = UserCreationFormExtended()
            return render_to_response(template_name, {
                'form': form,
                'title': 'KLP User',
                'legend': 'Karnataka Learning Partnership',
                'entry': 'Add', },
                context_instance=RequestContext(request))
    else:

        # if use is not login and user is not super user or not in admin group

        return HttpResponseRedirect('/login/')


def add_user_done(request):
    """ To Show User Creation done page"""

    return render_to_response('viewtemplates/userAction_done.html', {
        'message': 'User Creation Successful',
        'title': 'KLP User',
        'legend': 'Karnataka Learning Partnership',
        'entry': 'Add', },
        context_instance=RequestContext(request))


def change_password(request,
                    template_name='viewtemplates/password_change_form.html',
                    post_change_redirect=None):
    """ To Change Password """

    user = request.user  # Get logged in user
    usrUrl = {'Data Entry Executive': '/home/',
              'Data Entry Operator': '/home/?respType=filter',
              'AdminGroup': '/home/?respType=userpermissions'}
    if user.is_superuser:
        returnUrl = '/home/'
    elif user.is_staff:
        returnUrl = '/home/?respType=programme'
    else:
        userGroup = user.groups.all()[0].name
        returnUrl = usrUrl[userGroup]
    if user.id is not None:

        # if user is logged in

        if post_change_redirect is None:
            post_change_redirect = \
                reverse('accounts_password_change_done')
        if request.method == 'POST':

            # if request method is post post data to form

            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():

                # if form is valid save data to change pwd.

                form.save()

                # redirects to password change done.

                return HttpResponseRedirect(post_change_redirect)
            else:
                return render_to_response(template_name, {
                    'form': form,
                    'returnUrl': returnUrl,
                    'title': 'KLP Change Password',
                    'legend': 'Karnataka Learning Partnership',
                    'entry': 'Add', },
                    context_instance=RequestContext(request))
        else:
            form = PasswordChangeForm(request.user)
            return render_to_response(template_name, {
                'form': form,
                'returnUrl': returnUrl,
                'title': 'KLP Change Password',
                'legend': 'Karnataka Learning Partnership',
                'entry': 'Add', },
                context_instance=RequestContext(request))
    else:
        return HttpResponseRedirect('/login/')


def change_password_done(
        request, template_name='viewtemplates/password_change_done.html'):
    """ To Show Password Change done page. """

    user = request.user
    usrUrl = {'Data Entry Executive': '/home/',
              'Data Entry Operator': '/home/?respType=filter',
              'AdminGroup': '/home/?respType=userpermissions'}
    if user.is_superuser:
        returnUrl = '/home/'
    elif user.is_staff:
        returnUrl = '/home/?respType=programme'
    else:
        userGroup = user.groups.all()[0].name
        returnUrl = usrUrl[userGroup]
    return render_to_response(template_name, {
        'returnUrl': returnUrl,
        'title': 'KLP Change Password',
        'legend': 'Karnataka Learning Partnership',
        'entry': 'Add', },
        context_instance=RequestContext(request))
