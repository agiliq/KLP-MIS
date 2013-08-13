from django.conf.urls import patterns, url

from .views import login, logout, klp_user_auth

urlpatterns = patterns('',
    url(r'^$', login),
    url(r'^login/?$', login, name="login"),
    url(r'^logout/?$', logout, name="logout"),
    url(r'^user/authentication/?$', klp_user_auth),
)
