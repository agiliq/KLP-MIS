from django.conf.urls import patterns, url

from .views import *

urlpatterns = patterns('',
    url(r'^$', index, name="index"),
    url(r'^login/$', login, name="login"),
    url(r'^logout/$', logout, name="logout"),
    url(r'^user/authentication/$', user_auth, name="user_auth"),
    url(r'^accounts/auth/user/add/$', add_user, name='accounts_add_user'),
    url(r'^accounts/auth/user/addNewUser_done/$', add_user_done, name='accounts_add_user_done'),
    url(r'^accounts/password/change/$', change_password, name='accounts_password_change'),
    url(r'^accounts/password/done/$', change_password_done, name='accounts_password_change_done'),
)
