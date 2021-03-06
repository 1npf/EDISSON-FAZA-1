"""
Django settings for npf project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(+qb#i3$1q=a@qy66w9up(0cogb@aa#3^a=vnamp#e_5xj-%x7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'auth.User'

# Application definition
SITE_ID = 1

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_select2',
    'django.contrib.sites',
    'fias',
    'mptt',
    # 'viewflow',
    # 'viewform',

    'npf.core.basicauth',
    'npf.core.modelaudit',
    'npf.core.workflow',
    'npf.core.printform',
    'npf.core.counter',
    'npf.core.xmin',
    'npf.contrib.common',
    'npf.contrib.address',
    'npf.contrib.dict',
    # 'npf.contrib.employee',
    'npf.contrib.dashboard',
    'npf.contrib.subject',
    # 'npf.contrib.account',
    # 'npf.contrib.worksheet',
    # 'npf.contrib.closing',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, '..', 'media/log.txt'),
        },
    },
    'loggers': {
        'npf.contrib.common': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

SERIALIZATION_MODULES = {
    'json-pretty': 'npf.contrib.common.serializers.json_pretty'
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'npf.core.basicauth.middleware.BasicAuthMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

ROOT_URLCONF = 'npf.urls'

WSGI_APPLICATION = 'npf.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'npf',
        'USER': 'postgres',
        'PASSWORD': 'dhjnrjvgjn',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DATETIME_FORMAT = 'd.m.Y H:i:s'
DATE_FORMAT = 'd.m.Y'
TIME_FORMAT = 'H:i:s'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

MEDIA_URL = '/media/'

ADMIN_MEDIA_PREFIX = '/media/'

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

# Fias integration settings
# https://github.com/Yuego/django-fias

FIAS_TABLES = ('landmark', 'houseint', 'house')

FIAS_DATABASE_ALIAS = 'default'
