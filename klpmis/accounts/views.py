from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import UserCreationFormExtended


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
    return render(request, 'login.html', context)


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


@login_required
def add_user(request,
             template_name='accounts/add_new_user.html',
             post_change_redirect=None):

    """ This method is used to create or add new user """
    user = request.user
    if user.is_superuser:
        context = {
            'title': 'KLP User',
            'entry': 'Add'
        }
        form = UserCreationFormExtended()
        context['form'] = form
        if post_change_redirect is None:
            post_change_redirect = reverse('accounts_add_user_done')
        if request.method == 'POST':
            form = UserCreationFormExtended(request.POST)
            context['form'] = form
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(post_change_redirect)
            return render(request, template_name, context)
        return render(request, template_name, context)
    messages.add_message(request, messages.warning,
                         'You should be a super user to add a user')
    return HttpResponseRedirect(reverse("login"))


def add_user_done(request):
    """ To Show User Creation done page"""

    context = {'message': 'User Creation Successful',
               'title': 'KLP User',
               'entry': 'Add'}
    return render(request, 'accounts/userAction_done.html', context)


def change_password(request,
                    template_name='accounts/password_change_form.html',
                    post_change_redirect=None):
    """ To Change Password """

    user = request.user
    usrUrl = {'Data Entry Executive': '/home/'}
    if user.is_superuser:
        returnUrl = '/home/'
    elif user.is_staff:
        returnUrl = '/home/?respType=programme'
    else:
        userGroup = user.groups.all()[0].name
        returnUrl = usrUrl[userGroup]
    if request.user.is_authenticated():

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
                context = {'form': form,
                           'returnUrl': returnUrl,
                           'title': 'KLP Change Password',
                           'entry': 'Add'}
                return render(request,
                              template_name,
                              context)
        else:
            form = PasswordChangeForm(request.user)
            context = {'form': form,
                       'returnUrl': returnUrl,
                       'title': 'KLP Change Password',
                       'entry': 'Add'}
            return render(request,
                          template_name,
                          context)
    else:
        return HttpResponseRedirect(reverse("login"))


def change_password_done(
        request, template_name='accounts/password_change_done.html'):
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
    context = {'returnUrl': returnUrl,
               'title': 'KLP Change Password',
               'entry': 'Add', }
    return render(request,
                  template_name, context)
