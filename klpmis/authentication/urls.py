from django.conf.urls import patterns, url

from .views import klp_login, klp_logout, klp_user_auth

urlpatterns = patterns('',
    url(r'^$', klp_login),
    url(r'^login/?$', klp_login, name="login"),
    url(r'^logout/?$', klp_logout, name="logout"),
    url(r'^user/authentication/?$', klp_user_auth),
)
