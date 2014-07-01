from base import *

DEBUG = False 
ALLOWED_HOSTS = '*.klp.org.in'
DB_NAME = get_env_variable('DB_NAME')
DB_USER = get_env_variable('DB_USER')
DB_PASSWORD = get_env_variable('DB_PASSWORD')

SECRET_KEY = get_env_variable('SECRET_KEY')

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.mailb.org'
EMAIL_PORT = 587
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')

REPORTMAIL_RECEIVER = ['rakesh@agiliq.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': '127.0.0.1',
        'PORT': '',
        'OPTIONS': {'autocommit': True},
    }
}
