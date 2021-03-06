from .defaults import INSTALLED_APPS
from django.contrib.admin import site

try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass

DEBUG = True

TEMPLATE_DEBUG = True

INSTALLED_APPS = ('django_extensions', 'grappelli',) + INSTALLED_APPS

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'npf',
        'USER': 'postgres',
        'PASSWORD': '123',
    }
}

STATIC_ROOT = ''

GRAPPELLI_ADMIN_TITLE = site.site_title