from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render


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
            user_url = {'Data Entry Executive': '/home/',
                        'Data Entry Operator': '/home/?respType=filter',
                        'AdminGroup': '/home/?respType=userpermissions'}
            if user.is_superuser or user.is_staff:
                return HttpResponseRedirect(reverse('home'))
            else:
                user_group = user.groups.all()[0].name
                return HttpResponseRedirect(user_url[user_group])
    context['form'] = form
    return render(request,
                  'login.html',
                  context)


def logout(request):
    """ This method is for user logout """

    django_logout(request)
    return HttpResponseRedirect(reverse('login'))


def klp_user_auth(request):
    """ This method checks, user is authenticated or not """
    return HttpResponse(request.user.is_authenticated())


def index(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('login'))
