"""
Django settings for inventory project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys
from settings_secret import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = (len(sys.argv) > 1 and sys.argv[1] == 'runserver')

ALLOWED_HOSTS = ['*']

if DEBUG:
    SSLIFY_DISABLE = True
    SECURE_SSL_REDIRECT = False
    HTTPS = 'http'
    HOST_NAME = 'localhost'
    HOST_PORT = '8000'
    BASE_URL = HTTPS + '://' + HOST_NAME + ':' + HOST_PORT
else:
    BASE_URL = 'https://www.mccstats.com'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webpack_loader',
    'halo'
]

MIDDLEWARE_CLASSES = [
    'sslify.middleware.SSLifyMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'halo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates/bundle')],  # Webpack Directory
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'halo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'whey2ez',
#         'USER': 'gethypebaby',
#         'PASSWORD': 'sol2133080',
#         'HOST': 'whey2ez.c8ifh9asotnn.us-east-1.rds.amazonaws.com',
#         'PORT': '3306'
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'halo',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306'
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "templates"),
)

WEBPACK_LOADER = {
    'DEFAULT': {
        'BUNDLE_DIR_NAME': 'bundle/',
        'STATS_FILE': os.path.join(BASE_DIR, 'webpack-stats.json'),
    }
}
# AUTH_USER_MODEL = 'whey2ez.models.StoreManager'
AUTHENTICATION_BACKENDS = (
    # 'django.contrib.auth.backends.ModelBackend',
    'halo.custom.MyCustomBackend',
)
STATIC_URL = '/templates/'
TEMPLATE = (os.path.join(BASE_DIR, 'templates'),)
