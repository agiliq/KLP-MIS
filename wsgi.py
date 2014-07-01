"""
WSGI config for demo_project project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys

activate_this = '/home/klp/klpmis/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))

sys.path.append('/home/klp/KLP-MIS/klpmis')

# We defer to a DJANGO_SETTINGS_MODULE already in the environment. This breaks
# if running multiple sites in the same mod_wsgi process. To fix this, use
# mod_wsgi daemon mode with each site in its own daemon process, or use
# os.environ["DJANGO_SETTINGS_MODULE"] = "demo_project.settings"
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "klpmis.settings.dev_settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
_application = get_wsgi_application()

def application(environ, start_response):
    for var in ['DJANGO_SETTINGS_MODULE', 'DB_NAME', 'DB_PASSWORD', 'DB_USER', 'SECRET_KEY', 'EMAIL_HOST_PASSWORD', 'EMAIL_HOST_USER']:
        os.environ[var] = environ.get(var, '')
    return _application(environ, start_response)

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)