from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('accounts.urls')),
    url(r'', include('utils.urls')),
    url(r'', include('klprestApi.TreeMenu')),
    url(r'', include('klprestApi.LanguageApi')),
    url(r'', include('klprestApi.ProgrammeApi')),
    url(r'', include('klprestApi.QuestionApi')),
    url(r'', include('klprestApi.StudentGroupApi')),
    url(r'', include('klprestApi.StudentApi')),
    url(r'', include('klprestApi.StaffApi')),
    url(r'', include('klprestApi.KLP_Permission')),
    url(r'', include('klprestApi.urls.urls')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
